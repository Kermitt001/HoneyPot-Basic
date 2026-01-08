import os
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Network
    SSH_PORT: int = 2222
    BIND_ADDRESS: str = "0.0.0.0"
    
    # Security
    MAX_AUTH_ATTEMPTS: int = 3
    BANNER_TEXT: str = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DB_PATH: str = "honeypot.db"
    LOG_FILE: str = "events.jsonl"
    HOST_KEY_FILE: str = "server.key"

    class Config:
        env_file = ".env"

settings = Settings()
