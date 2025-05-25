import json
import os
from datetime import datetime, timedelta

PROFILE_PATH = "data/user_profile.json"

default_profile = {
    "name": "Beloved",
    "bible_version": "ESV",
    "spiritual_focus": ["grace", "identity", "faith"],
    "mood": "neutral",
    "streak": {
        "current": 0,
        "longest": 0,
        "last_journal_date": None
    }
}

def load_user_profile():
    if not os.path.exists(PROFILE_PATH):
        save_user_profile(default_profile)
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def save_user_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

def update_user_profile_field(field, value):
    profile = load_user_profile()
    profile[field] = value
    save_user_profile(profile)

def update_streak(latest_date_str):
    profile = load_user_profile()
    streak = profile.get("streak", {"current": 0, "longest": 0, "last_journal_date": None})
    
    today = datetime.utcnow().date()
    latest_date = datetime.fromisoformat(latest_date_str).date()
    last_date_str = streak.get("last_journal_date")
    last_date = datetime.fromisoformat(last_date_str).date() if last_date_str else None

    # Only update if journaling today
    if latest_date != today:
        return

    if last_date == today - timedelta(days=1):
        streak["current"] += 1
    elif last_date != today:
        streak["current"] = 1

    streak["longest"] = max(streak["longest"], streak["current"])
    streak["last_journal_date"] = today.isoformat()
    profile["streak"] = streak
    save_user_profile(profile)
