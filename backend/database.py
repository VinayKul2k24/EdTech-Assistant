import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_query TEXT,
            agent_used VARCHAR(50),
            response TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def log_interaction(query: str, agent: str, response: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO interactions (user_query, agent_used, response) VALUES (%s, %s, %s)",
        (query, agent, response)
    )
    conn.commit()
    cursor.close()
    conn.close()