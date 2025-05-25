from backend.utils.user_profile import load_user_profile
from backend.utils.journal import find_related_journals

def get_rhema(verse: str, doctrine_summary: str) -> str:
    profile = load_user_profile()
    name = profile.get("name", "Beloved")
    focus_areas = profile.get("spiritual_focus", [])
    mood = profile.get("mood", "neutral")

    focus_text = ", ".join(focus_areas) if focus_areas else "a general desire to grow spiritually"
    related_entries = find_related_journals(focus_areas)

    # Format past entries
    past = ""
    if related_entries:
        past += "📜 Here are a few of your past reflections related to this:\n\n"
        for entry in related_entries:
            past += f"- {entry['timestamp'][:10]}: {entry['journal'][:200]}...\n"

    prompt = f"""
👤 Hello {name},

📖 Studying: "{verse}"

✝️ Doctrinal insight:
{doctrine_summary}

🧠 Mood: "{mood}"
🎯 Focus: {focus_text}

{past}

🗣️ Reflect with the Holy Spirit:
1. What new truth is being highlighted now?
2. Does this connect to any past season?
3. What might God be inviting you into?

📍 Write or pray in response. Let it become a conversation.
"""

    return prompt
