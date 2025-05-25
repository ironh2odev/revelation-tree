from backend.utils.user_profile import load_user_profile
from backend.utils.journal import find_related_journals

def get_application(verse: str, rhema: str):
    profile = load_user_profile()
    name = profile.get("name", "Beloved")
    focus = ", ".join(profile.get("spiritual_focus", []))
    mood = profile.get("mood", "neutral")
    
    # Optional: Reflect on recent themes to tailor application
    related_entries = find_related_journals(profile.get("spiritual_focus", []))
    last_journal = related_entries[0]["journal"] if related_entries else ""

    declaration = f"I declare that I am walking in God's truth. I receive His {focus or 'grace'} today."
    prayer = (
        f"Father, thank You for speaking to me through {verse}. "
        f"Even in this {mood} season, I know You are near. Help me walk in what You just revealed."
    )
    action = f"Take 5 minutes today to meditate on {verse} and ask the Holy Spirit how to live it out practically."

    challenge = ""
    if last_journal:
        challenge = "Re-read your last journal and ask: 'How has God been connecting the dots over time?'"

    return {
        "declaration": declaration,
        "prayer": prayer,
        "life_action": action,
        "journal_challenge": challenge,
    }
