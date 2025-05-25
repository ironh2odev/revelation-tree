from backend.rag.retriever import query_index

# Simple keyword-based theme classifier
def classify_themes(text: str) -> list:
    themes = {
        "grace": ["grace", "undeserved", "gift", "favor"],
        "identity": ["in Christ", "new creation", "righteousness", "child of God"],
        "faith": ["believe", "faith", "trust", "confidence"],
        "healing": ["heal", "restoration", "health"],
        "freedom": ["free", "liberty", "deliverance"],
        "kingdom": ["kingdom", "authority", "rule", "dominion"]
    }
    tags = set()
    lowered = text.lower()
    for theme, keywords in themes.items():
        if any(k in lowered for k in keywords):
            tags.add(theme)
    return list(tags)

def get_doctrine(verse: str) -> str:
    try:
        retrieved_insights = query_index(verse)
    except Exception as e:
        return f"❌ Could not retrieve insights for `{verse}`. Reason: {str(e)}"

    if not retrieved_insights:
        return f"ℹ️ No doctrinal commentary found for `{verse}`. Try a broader verse or keyword."

    response = f"📖 *Doctrinal Insight for:* `{verse}`\n\n"
    response += "This verse reveals the following spiritual truths:\n\n"

    combined = ""
    for i, chunk in enumerate(retrieved_insights, start=1):
        chunk = chunk.strip()
        response += f"**{i}.** {chunk}\n\n"
        combined += f"{chunk} "

    # Tag dominant themes
    tags = classify_themes(combined)
    if tags:
        tag_list = ", ".join([f"`{t}`" for t in tags])
        response += f"_Themes emphasized: {tag_list}_"
    else:
        response += "_Themes emphasized: general spiritual principles._"

    return response
