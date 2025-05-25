# backend/utils/suggest_tags.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TAG_CANDIDATES = ["grace", "identity", "faith", "healing", "freedom", "love"]

def suggest_tags(text, top_n=3):
    documents = TAG_CANDIDATES + [text]
    tfidf = TfidfVectorizer().fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf[-1:], tfidf[:-1])
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    suggested_tags = [TAG_CANDIDATES[i] for i, _ in sim_scores[:top_n]]
    return suggested_tags
