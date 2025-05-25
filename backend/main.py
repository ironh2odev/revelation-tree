from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.user_profile import (
    load_user_profile,
    save_user_profile,
    update_user_profile_field
)
from backend.utils.journal import (
    save_journal_entry,
    load_journals,
    update_journal_entry  # ✅ NEW
)
from backend.utils.theme_tracker import track_themes
from backend.agents.context_agent import get_context
from backend.agents.doctrine_agent import get_doctrine
from backend.agents.rhema_agent import get_rhema
from backend.agents.application_agent import get_application
from backend.utils.suggest_tags import suggest_tags
from collections import Counter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/study")
async def study(request: Request):
    data = await request.json()
    verse = data.get("verse")

    context = get_context(verse)
    doctrine = get_doctrine(verse)
    rhema = get_rhema(verse, doctrine)
    application = get_application(verse, rhema)

    return {
        "context": context,
        "doctrine": doctrine,
        "rhema": rhema,
        "application": application,
    }

@app.post("/journal")
async def journal_entry(request: Request):
    data = await request.json()
    save_journal_entry(data)
    return {"message": "Saved"}

@app.post("/update_journal")  # ✅ NEW endpoint
async def update_journal(request: Request):
    data = await request.json()
    uuid = data.get("uuid")
    updated = update_journal_entry(uuid, data)
    return {"success": updated}

@app.get("/journals")
def get_journals():
    return load_journals()

@app.get("/themes")
def get_themes():
    return track_themes()

@app.get("/profile")
def get_profile():
    return load_user_profile()

@app.post("/profile")
async def update_profile(request: Request):
    data = await request.json()
    for k, v in data.items():
        update_user_profile_field(k, v)
    return {"message": "Profile updated!"}

@app.post("/suggest_tags")
async def suggest_tags_endpoint(request: Request):
    data = await request.json()
    journal_text = data.get("text", "")
    tags = suggest_tags(journal_text)
    return {"tags": tags}

@app.get("/journal_stats")
def get_journal_stats():
    journals = load_journals()
    if not journals:
        return {
            "total": 0,
            "most_common_tag": None,
            "most_common_verse": None,
            "earliest": None,
            "latest": None
        }

    tags = [tag for entry in journals for tag in entry.get("tags", [])]
    verses = [entry.get("verse", "") for entry in journals]
    timestamps = [entry.get("timestamp") for entry in journals]

    return {
        "total": len(journals),
        "most_common_tag": Counter(tags).most_common(1)[0][0] if tags else None,
        "most_common_verse": Counter(verses).most_common(1)[0][0] if verses else None,
        "earliest": min(timestamps),
        "latest": max(timestamps)
    }
