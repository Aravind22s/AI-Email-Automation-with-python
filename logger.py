import json
import os
from datetime import datetime

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "logs.json")

def load_logs():
    if os.path.exists(LOG_FILE_PATH):
        return []
    with open(LOG_FILE_PATH, "r") as file:
            return json.load(file)
        
def save_logs(logs):
    with open(LOG_FILE_PATH, "w") as file:
        json.dump(logs, file, indent=4)
        
def is_processed(message_id):
    logs = load_logs()
    for log in logs:
        if log["message_id"] == message_id:
            return True
    return False

def save_email_log(message_id, sender, suject, status):
    logs = load_logs()
    log_entry = {
        "message_id": message_id,
        "sender": sender,
        "subject": suject,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    logs.append(log_entry)
    save_logs(logs)