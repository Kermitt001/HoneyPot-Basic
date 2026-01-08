import json
import logging
from datetime import datetime
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("honeypot.system.log")
    ]
)

class EventLogger:
    def __init__(self):
        self.log_file = settings.LOG_FILE

    def log_event(self, event_type: str, data: dict):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")

event_logger = EventLogger()
