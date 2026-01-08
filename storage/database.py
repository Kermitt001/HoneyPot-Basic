import sqlite3
import logging
from config.settings import settings

logger = logging.getLogger("honeypot.storage")

def init_db():
    """Initialize the SQLite database schema."""
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    # Sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        start_time TEXT,
        end_time TEXT,
        src_ip TEXT,
        src_port INTEGER,
        client_version TEXT,
        username TEXT,
        password TEXT,
        success BOOLEAN
    )
    ''')

    # Commands table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        timestamp TEXT,
        command TEXT,
        response_type TEXT,
        mitre_tactic TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id)
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {settings.DB_PATH}")

def insert_session(session_data: dict):
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO sessions (session_id, start_time, end_time, src_ip, src_port, client_version, username, password, success)
    VALUES (:session_id, :start_time, :end_time, :src_ip, :src_port, :client_version, :username, :password, :success)
    ''', session_data)
    conn.commit()
    conn.close()

def insert_command(command_data: dict):
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO commands (session_id, timestamp, command, response_type, mitre_tactic)
    VALUES (:session_id, :timestamp, :command, :response_type, :mitre_tactic)
    ''', command_data)
    conn.commit()
    conn.close()
