from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
import mysql.connector

# ---------------- CONFIG ----------------
SECRET_KEY = "supersecretkey"       # ⚠️ change this, or load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------------- MODELS ----------------
class UserIn(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Idea(BaseModel):
    title: str
    category: str
    members: str | None = None
    description: str | None = None
    status: str = "new"
    completion_percentage: int = 0

# ---------------- UTILS ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="Welcome01",
        database="idea_manager"
    )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ---------------- AUTH ROUTES ----------------
@app.post("/register")
def register(user: UserIn):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed = bcrypt.hash(user.password)
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s,%s)",
            (user.username, hashed)
        )
        conn.commit()
        return {"msg": "User registered"}
    except:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        cur.close()
        conn.close()

@app.post("/login", response_model=Token)
def login(user: UserIn):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (user.username,))
    db_user = cur.fetchone()
    cur.close()
    conn.close()

    if not db_user or not bcrypt.verify(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ---------------- IDEA ROUTES ----------------
@app.post("/ideas")
def create_idea(idea: Idea, user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO ideas (title, category, members, description, status, completion_percentage, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        idea.title,
        idea.category,
        idea.members,
        idea.description,
        idea.status,
        idea.completion_percentage,
        user["id"],
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Idea created successfully"}

@app.get("/ideas")
def get_ideas(user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ideas WHERE created_by = %s", (user["id"],))
    ideas = cursor.fetchall()
    cursor.close()
    conn.close()
    return ideas


@app.get("/ideas/{idea_id}")
def get_idea(idea_id: int, user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ideas WHERE id = %s AND created_by = %s", (idea_id, user["id"]))
    idea = cursor.fetchone()
    cursor.close()
    conn.close()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return idea

@app.put("/ideas/{idea_id}")
def update_idea(idea_id: int, idea: Idea, user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE ideas
        SET title=%s, category=%s, members=%s, description=%s, status=%s, completion_percentage=%s
        WHERE id=%s AND created_by=%s
        """,
        (
            idea.title,
            idea.category,
            idea.members,
            idea.description,
            idea.status,
            idea.completion_percentage,
            idea_id,
            user["id"]
        )
    )
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Idea not found or not authorized")

    return {"message": "Idea updated successfully"}




@app.delete("/ideas/{idea_id}")
def delete_idea(idea_id: int, user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ideas WHERE id = %s AND created_by = %s",
        (idea_id, user["id"])
    )
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Idea not found or not authorized")

    return {"message": "Idea deleted successfully"}


# ---------------- MIDDLEWARE ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
