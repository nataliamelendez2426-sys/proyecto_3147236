# basedatos/db.py 
import mysql.connector

def get_connection():
    """Devuelve una conexión nueva a la base de datos."""
    return mysql.connector.connect(
        user='root',
        password='2426',
        host='localhost',
        database='tienda_db',
    )
