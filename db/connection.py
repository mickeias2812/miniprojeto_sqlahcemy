import mysql.connector

db_config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': '',
    'database': 'db_trabalho3b'
}

def get_connection():
    return mysql.connector.connect(**db_config)
