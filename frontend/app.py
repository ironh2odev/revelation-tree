import streamlit as st
import requests
from datetime import datetime, timedelta
from dateutil import parser
import json

if "journal_text" not in st.session_state:
    st.session_state.journal_text = ""
if "focus" not in st.session_state:
    st.session_state.focus = []
if "edit_entry" not in st.session_state:
    st.session_state.edit_entry = None
if "last_verse" not in st.session_state:
    st.session_state.last_verse = ""
if "study_result" not in st.session_state:
    st.session_state.study_result = {}

st.set_page_config(page_title="Revelation Tree", page_icon="🌳", layout="wide")

# Sidebar: Streak Display
try:
    profile_res = requests.get("http://localhost:8000/profile")
    if profile_res.status_code == 200:
        profile = profile_res.json()
        name = profile.get("name", "Beloved")
        streak = profile.get("streak", {})
        current = streak.get("current", 0)
        longest = streak.get("longest", 0)
        weekly_focus = profile.get("weekly_focus")
        if current > 0:
            streak_display = f"🔥 {name} ({current} day{'s' if current > 1 else ''})"
        elif longest >= 3:
            streak_display = f"👑 {name} (Longest: {longest} days)"
        else:
            streak_display = f"🌱 {name}"
        st.sidebar.title("🌳 Revelation Tree")
        st.sidebar.markdown(f"**{streak_display}**")
        if weekly_focus:
            st.sidebar.markdown(f"✨ **Weekly Focus:** `{weekly_focus}`")
    else:
        st.sidebar.title("🌳 Revelation Tree\n🌱 Beloved")
except Exception:
    st.sidebar.title("🌳 Revelation Tree\n🌱 Beloved")

page = st.sidebar.radio("Navigate", ["Study Verse", "Journal Timeline"])

# Sidebar: Profile
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 User Profile")
with st.sidebar.form("profile_form", clear_on_submit=False):
    name = st.text_input("Name", value=profile.get("name", "Beloved") if 'profile' in locals() else "Beloved")
    version = st.selectbox("Bible Version", ["ESV", "NKJV", "TPT"])
    focus_input = st.multiselect("Spiritual Focus Areas", ["grace", "identity", "faith", "healing", "freedom", "love"], default=st.session_state.focus)
    submitted = st.form_submit_button("Save Profile")
    if submitted:
        profile_data = {"name": name, "bible_version": version, "spiritual_focus": focus_input}
        try:
            res = requests.post("http://localhost:8000/profile", json=profile_data)
            if res.status_code == 200:
                st.session_state.focus = focus_input
                st.success("Profile updated!")
            else:
                st.error("Failed to update profile.")
        except Exception as e:
            st.error(f"Connection error: {e}")

# Study Verse Page
if page == "Study Verse":
    st.markdown("## 📖 Study Verse")
    st.markdown("A Spirit-led layered study (Context → Doctrine → Rhema → Application)")

    verse = st.text_input("Enter a Bible Verse (e.g., John 3:16)", value=st.session_state.last_verse)

    if st.button("🔍 Study"):
        if not verse.strip():
            st.warning("Please enter a verse.")
        else:
            try:
                res = requests.post("http://localhost:8000/study", json={"verse": verse})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.study_result = data
                    st.session_state.last_verse = verse
                else:
                    st.error("Failed to retrieve study content.")
            except Exception as e:
                st.error(f"Study error: {e}")

    if st.session_state.study_result:
        result = st.session_state.study_result
        st.markdown("### 🧠 Context")
        st.write(result.get("context", "No context available."))
        st.markdown("### 📜 Doctrine")
        st.write(result.get("doctrine", "No doctrine available."))
        st.markdown("### 🔥 Rhema")
        st.write(result.get("rhema", "No rhema available."))
        st.markdown("### 🪴 Application")
        app = result.get("application", {})
        st.markdown(f"**🗣 Declaration:** {app.get('declaration', '—')}")
        st.markdown(f"**🙏 Prayer:** {app.get('prayer', '—')}")
        st.markdown(f"**🔥 Action Step:** {app.get('life_action', '—')}")
        st.markdown(f"**📓 Journal Prompt:** {app.get('journal_challenge', '—')}")

        st.markdown("### ✍️ Your Journal Response")
        journal_text = st.text_area("Reflect here", value=st.session_state.journal_text, height=150)

        if st.button("💾 Save Journal"):
            if not journal_text.strip():
                st.warning("Please write something before saving.")
            else:
                try:
                    tag_res = requests.post("http://localhost:8000/suggest_tags", json={"text": journal_text})
                    tags = tag_res.json().get("tags", []) if tag_res.status_code == 200 else st.session_state.focus
                except:
                    tags = st.session_state.focus or []
                payload = {
                    "name": name or "Beloved",
                    "verse": st.session_state.last_verse,
                    "timestamp": datetime.utcnow().isoformat(),
                    "journal": journal_text.strip(),
                    "tags": tags
                }
                try:
                    jr = requests.post("http://localhost:8000/journal", json=payload)
                    if jr.status_code == 200:
                        st.success("Journal entry saved!")
                        st.session_state.journal_text = ""
                    else:
                        st.error("Failed to save journal.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.session_state.journal_text = journal_text

# Journal Timeline Page with Export
if page == "Journal Timeline":
    st.markdown("## 🗂️ Journal Timeline")
    try:
        entries = requests.get("http://localhost:8000/journals").json()
        filtered = sorted(entries, key=lambda e: parser.isoparse(e["timestamp"]), reverse=True)

        if not filtered:
            st.warning("No journal entries available.")
        else:
            for entry in filtered:
                with st.expander(f"{entry.get('verse')} • {parser.isoparse(entry['timestamp']).strftime('%b %d, %Y')}"):
                    st.markdown(f"**Tags:** {', '.join(f'`{t}`' for t in entry.get('tags', []))}")
                    st.write(entry.get("journal", ""))

            st.markdown("### 📤 Export Journals")
            export_format = st.selectbox("Choose format", ["JSON", "Markdown"])
            if st.button("⬇️ Export Now"):
                if export_format == "JSON":
                    st.download_button("Download .json", json.dumps(filtered, indent=2), file_name="journals.json")
                else:
                    md_text = ""
                    for e in filtered:
                        ts = parser.isoparse(e["timestamp"]).strftime('%Y-%m-%d')
                        md_text += f"### {e.get('verse', '')} ({ts})\n"
                        if e.get("tags"):
                            md_text += f"`Tags:` {', '.join(e['tags'])}\n\n"
                        md_text += f"{e['journal']}\n\n---\n\n"
                    st.download_button("Download .md", md_text, file_name="journals.md")

    except Exception as e:
        st.error(f"Error loading timeline: {e}")
