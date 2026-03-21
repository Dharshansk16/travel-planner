import re

VALID_TOOLS = [
    "get_nearby_locations",
    "estimate_cost",
    "fetch_weather",
    "get_rating",
    "finalize"
]

def extract_action(text: str) -> str:
    if not text:
        return "finalize"

    # Pattern 1: LLM follows format — ACTION: get_nearby_locations
    match = re.search(r"ACTION:\s*(\S+)", text, re.IGNORECASE)
    if match:
        raw = match.group(1).strip().lower().strip("().,:")
        for tool in VALID_TOOLS:
            if tool in raw:
                return tool

    # Pattern 2: LLM mentioned tool name without ACTION: label
    text_lower = text.lower()
    for tool in VALID_TOOLS:
        if tool in text_lower:
            return tool

    # Pattern 3: LLM said it is done without saying finalize
    done_words = ["enough", "sufficient", "done", "complete", "ready", "proceed"]
    for word in done_words:
        if word in text_lower:
            return "finalize"

    # Default — always return something valid
    return "finalize"