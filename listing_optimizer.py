# listing_optimizer.py
#
# Simple rule-based optimizer. You can later replace these
# functions with calls to a real LLM (OpenAI, etc.)

COMMON_BAD_WORDS = ["cheap", "best", "wow", "free"]
MAX_TITLE_LENGTH = 80

def optimize_title(title):
    if not title:
        return title

    t = title.strip()

    # Remove ALL CAPS spammy look
    t = t.title()

    # Remove bad words
    for w in COMMON_BAD_WORDS:
        t = t.replace(w.title(), "").replace(w.upper(), "").replace(w.lower(), "")

    # Trim and cut to max length
    t = " ".join(t.split())
    if len(t) > MAX_TITLE_LENGTH:
        t = t[:MAX_TITLE_LENGTH - 3] + "..."

    return t

def optimize_description(desc):
    if not desc:
        return desc

    lines = desc.strip().splitlines()
    cleaned = [ln.strip() for ln in lines if ln.strip()]

    # Basic formatting
    return "\n".join(cleaned)
