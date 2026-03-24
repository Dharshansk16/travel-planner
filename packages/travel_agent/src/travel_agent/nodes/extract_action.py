import re

VALID_TOOLS = [
    "search_places",
    "search_flights",
    "search_hotels",
    "fetch_weather",
    "finalize"
]

def extract_action(text: str) -> str:
    if not text:
        return "finalize"

    match = re.search(r"ACTION:\s*(\S+)", text, re.IGNORECASE)
    if match:
        raw = match.group(1).strip().lower().strip("().,:")
        for tool in VALID_TOOLS:
            if tool in raw:
                return tool

    text_lower = text.lower()
    for tool in VALID_TOOLS:
        if tool in text_lower:
            return tool

    done_words = ["enough", "sufficient", "done", "complete", "ready", "proceed"]
    for word in done_words:
        if word in text_lower:
            return "finalize"

    return "finalize"