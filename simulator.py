"""simulator.py - the main simulate() flow: scan -> decide -> mask -> log."""
from detector import scan
from policy import decide, action_for
from logger import log_event

CHANNELS = ["email", "usb", "cloud", "chat"]


def mask(text, hits):
    """Replace every value whose rule is MASK with asterisks."""
    for name, val in hits:
        if action_for(name) == "MASK":
            text = text.replace(val, "*" * len(val))
    return text


def simulate(user, channel, payload):
    """Single entry point. Returns (action, payload, hits).

    - BLOCK  -> payload is withheld (empty string)
    - MASK   -> payload is returned with sensitive values hidden
    - WARN / ALLOW -> payload is returned unchanged
    """
    if channel not in CHANNELS:
        channel = "chat"
    payload = payload or ""

    hits = scan(payload)
    action = decide(hits)

    if action == "MASK":
        payload = mask(payload, hits)
    elif action == "BLOCK":
        payload = ""

    log_event(user, channel, hits, action)
    return action, payload, hits
