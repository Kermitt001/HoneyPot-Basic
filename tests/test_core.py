import pytest
import os
import sqlite3
import time
from honeypot.shell import HoneypotShell
from storage.database import init_db
from config.settings import settings

# Setup dummy env
os.environ["DB_PATH"] = "test_honeypot.db"
settings.DB_PATH = "test_honeypot.db"

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup
    if os.path.exists("test_honeypot.db"):
        os.remove("test_honeypot.db")
    init_db()
    yield
    # Teardown
    if os.path.exists("test_honeypot.db"):
        os.remove("test_honeypot.db")

def test_shell_commands():
    shell = HoneypotShell("test_session")
    
    # Test valid command
    resp = shell.handle_command("whoami")
    assert "root" in resp
    
    # Test fake command
    resp = shell.handle_command("xyz")
    assert "not found" in resp

def test_db_logging():
    shell = HoneypotShell("test_session_db")
    shell.handle_command("ls")
    
    conn = sqlite3.connect("test_honeypot.db")
    c = conn.cursor()
    c.execute("SELECT command FROM commands WHERE session_id='test_session_db'")
    cmds = c.fetchall()
    conn.close()
    
    assert len(cmds) == 1
    assert cmds[0][0] == "ls"
