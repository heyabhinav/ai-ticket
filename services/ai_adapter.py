"""
Adapter placeholder for future Azure integration.
Expose a simple function `classify_text(text: str)` which returns (category, confidence).
Right now it returns a dummy response for development.
"""
from typing import Tuple

def classify_text(text: str) -> Tuple[str, float]:
    # TODO: replace with Azure call
    # Simple heuristics for dev: keyword mapping
    t = text.lower()
    if "db" in t or "database" in t or "postgres" in t:
        return ("Database", 0.9)
    if "network" in t or "dns" in t or "router" in t:
        return ("Network", 0.88)
    if "login" in t or "password" in t or "sso" in t:
        return ("Access", 0.92)
    return ("Other", 0.6)