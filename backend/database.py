import mysql.connector
from mysql.connector import pooling

dbconfig = {
    "user": "root",
    "password": "Welcome01",
    "host": "db",
    "database": "idea_manager"
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                              pool_size=5,
                                              **dbconfig)

def get_connection():
    return connection_pool.get_connection()
