"""detector.py - finds sensitive data in text using regex + Luhn check."""
import re

# Order matters: more specific / critical types first, so that overlapping
# matches (e.g. a card number also looking like an Aadhaar) are reported once.
PATTERNS = {
    "CREDIT_CARD": r"\b(?:\d[ -]?){13,16}\b",
    "API_KEY": r"\b(?:sk|key)_[A-Za-z0-9]{16,}\b",
    "AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "PAN": r"\b[A-Z]{5}\d{4}[A-Z]\b",
    "PHONE": r"(?:\+91[\s-]?)?\b[6-9]\d{4}[\s-]?\d{5}\b",
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
}

SEVERITY = {
    "CREDIT_CARD": "Critical",
    "API_KEY": "Critical",
    "AADHAAR": "Critical",
    "PAN": "High",
    "PHONE": "Medium",
    "EMAIL": "Low",
}


def luhn_ok(num):
    """Return True if the digits in `num` pass the Luhn checksum."""
    d = [int(c) for c in num if c.isdigit()]
    if len(d) < 13:
        return False
    d.reverse()
    total = sum(d[0::2])
    for x in d[1::2]:
        total += sum(divmod(x * 2, 10))
    return total % 10 == 0


def scan(text):
    """Return a list of (type, value) findings found in `text`."""
    hits = []
    used = []  # (start, end) spans already claimed by an earlier pattern
    if not text:
        return hits

    for name, rx in PATTERNS.items():
        for m in re.finditer(rx, text):
            start, end = m.span()
            value = m.group()

            # skip anything overlapping a span already reported
            if any(start < e and end > s for s, e in used):
                continue

            # a card number is kept only if it passes the Luhn check
            if name == "CREDIT_CARD" and not luhn_ok(value):
                continue

            hits.append((name, value))
            used.append((start, end))
    return hits
