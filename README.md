# 🌳 Revelation Tree

Revelation Tree is a Spirit-led Bible study and journaling app powered by FastAPI and Streamlit. It guides users through a layered study approach — Context → Doctrine → Rhema → Application — while helping them journal insights, track spiritual growth, and stay rooted in their identity in Christ.

## ✨ Features
- Contextual, doctrinal, and prophetic breakdown of any Bible verse
- Journal with AI-tag suggestions
- Streak and weekly focus tracking
- View, filter, and edit past entries
- Tag analytics and verse history

## 🚀 Run Locally

```bash
# Backend
cd backend
uvicorn backend.main:app --reload

# Frontend (in new terminal)
cd frontend
streamlit run frontend/app.py
