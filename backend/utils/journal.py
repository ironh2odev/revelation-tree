import json
import os
import uuid
from datetime import datetime, timedelta
from dateutil import parser
from .user_profile import load_user_profile, save_user_profile

JOURNAL_PATH = "data/journals.json"

def save_journal_entry(entry):
    try:
        with open(JOURNAL_PATH, "r") as f:
            journals = json.load(f)
    except FileNotFoundError:
        journals = []

    if "uuid" not in entry:
        entry["uuid"] = str(uuid.uuid4())

    entry["timestamp"] = datetime.utcnow().isoformat()
    journals.append(entry)

    with open(JOURNAL_PATH, "w") as f:
        json.dump(journals, f, indent=2)

    update_streak(journals)
    update_weekly_focus(journals)

def load_journals():
    try:
        with open(JOURNAL_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def update_journal_entry(uuid_value, new_data):
    try:
        with open(JOURNAL_PATH, "r") as f:
            journals = json.load(f)
    except FileNotFoundError:
        return False

    updated = False
    for entry in journals:
        if entry.get("uuid") == uuid_value:
            entry.update(new_data)
            entry["timestamp"] = datetime.utcnow().isoformat()
            updated = True
            break

    if updated:
        with open(JOURNAL_PATH, "w") as f:
            json.dump(journals, f, indent=2)
        update_streak(journals)
        update_weekly_focus(journals)

    return updated

def find_related_journals(query_tags):
    from .theme_tracker import extract_tags_from_journal

    journals = load_journals()
    related = []

    for entry in journals:
        tags = extract_tags_from_journal(entry.get("journal", ""))
        if any(tag in tags for tag in query_tags):
            related.append(entry)

    return sorted(related, key=lambda x: x["timestamp"], reverse=True)[:3]

def update_streak(journals):
    profile = load_user_profile()
    timestamps = sorted({parser.isoparse(e["timestamp"]).date() for e in journals}, reverse=True)

    today = datetime.utcnow().date()
    streak = 0
    longest = 0
    count = 0
    previous = None

    for date in timestamps:
        if previous is None or previous - date == timedelta(days=1):
            count += 1
        else:
            longest = max(longest, count)
            count = 1
        if date == today or (previous is None and date == today - timedelta(days=1)):
            streak = count
        previous = date

    longest = max(longest, count)
    profile["streak"] = {
        "current": streak,
        "longest": longest
    }
    save_user_profile(profile)

def update_weekly_focus(journals):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    tag_counter = {}

    for entry in journals:
        ts = parser.isoparse(entry["timestamp"])
        if ts >= one_week_ago:
            for tag in entry.get("tags", []):
                tag_counter[tag] = tag_counter.get(tag, 0) + 1

    top_tag = max(tag_counter, key=tag_counter.get) if tag_counter else None
    profile = load_user_profile()
    profile["weekly_focus"] = top_tag
    save_user_profile(profile)
