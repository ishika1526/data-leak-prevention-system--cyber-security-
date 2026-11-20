"""logger.py - stores event records and raises admin alerts.

Only the data TYPES are stored, never the raw sensitive values.
"""
import json
from datetime import datetime

LOGS = []
ALERTS = []


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def alert_admin(entry):
    """Simulated admin alert (printed and kept in memory)."""
    msg = (f"[ALERT] {entry['time']} - BLOCKED {entry['types']} "
           f"from {entry['user']} via {entry['channel']}")
    ALERTS.append(msg)
    print(msg)


def log_event(user, channel, hits, action):
    entry = {
        "time": now(),
        "user": user,
        "channel": channel,
        "types": [h[0] for h in hits],
        "action": action,
    }
    LOGS.append(entry)
    if action == "BLOCK":
        alert_admin(entry)
    return entry


def save_logs(path="logs.json"):
    """Optional: write the event log to disk."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(LOGS, f, indent=2)
