from pydantic import BaseModel

class Idea(BaseModel):
    short_desc: str
    category: str
    members: str
    description: str
    status: str
    completion: int
    created_by: str
