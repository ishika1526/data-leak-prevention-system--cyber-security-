"""policy.py - maps each data type to an action and picks the strictest one."""
import json
import os

DEFAULT_RULES = {
    "CREDIT_CARD": "BLOCK",
    "AADHAAR": "BLOCK",
    "API_KEY": "BLOCK",
    "PAN": "MASK",
    "PHONE": "MASK",
    "EMAIL": "WARN",
}

# Actions ranked from least to most strict
ORDER = ["ALLOW", "WARN", "MASK", "BLOCK"]


def load_rules(path="policies.json"):
    """Load rules from policies.json; fall back to defaults if missing/invalid."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                rules = json.load(f)
            if isinstance(rules, dict):
                return rules
        except (OSError, json.JSONDecodeError):
            pass
    return dict(DEFAULT_RULES)


RULES = load_rules()


def action_for(data_type):
    """Action for one data type. Unknown types default to ALLOW."""
    return RULES.get(data_type, "ALLOW")


def decide(hits):
    """Return the strictest action required by all findings."""
    worst = "ALLOW"
    for name, _ in hits:
        a = action_for(name)
        if a in ORDER and ORDER.index(a) > ORDER.index(worst):
            worst = a
    return worst
