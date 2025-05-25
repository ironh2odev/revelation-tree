import re
from backend.utils.journal import load_journals

# Example spiritual theme keywords
THEME_KEYWORDS = {
    "grace": ["grace", "undeserved", "gift", "favor"],
    "identity": ["who I am", "son", "daughter", "beloved", "chosen"],
    "faith": ["faith", "believe", "trust", "confidence"],
    "healing": ["heal", "healing", "restore", "wholeness"],
    "freedom": ["free", "freedom", "delivered", "chains broken"],
    "love": ["love", "loved", "loving", "affection"]
}

def extract_tags_from_journal(text: str):
    tags = set()
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE):
                tags.add(theme)
                break
    return list(tags)

def track_themes():
    journals = load_journals()
    theme_count = {}
    for entry in journals:
        content = entry.get("content", "")
        tags = extract_tags_from_journal(content)
        for tag in tags:
            theme_count[tag] = theme_count.get(tag, 0) + 1
    return theme_count
