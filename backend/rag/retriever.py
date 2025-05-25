import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings  # ✅ Updated from deprecated langchain_community
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables from .env
load_dotenv()

DATA_DIR = "data/commentary"
CHROMA_DIR = "data/chroma_db"


def load_documents():
    """Load all .txt files from the commentary folder as LangChain documents."""
    docs = []
    if not os.path.exists(DATA_DIR):
        print(f"[retriever] ❌ DATA_DIR '{DATA_DIR}' not found.")
        return docs

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(path)
            docs.extend(loader.load())
            print(f"[retriever] ✅ Loaded {filename}")
    return docs


def create_vector_store():
    """Create and persist a Chroma vector store from commentary documents."""
    docs = load_documents()
    if not docs:
        raise ValueError("[retriever] No documents to index.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vectordb.persist()
    print("[retriever] ✅ Vectorstore created and saved.")
    return vectordb


def load_vector_store():
    """Load Chroma vector store from disk."""
    if not os.path.exists(CHROMA_DIR):
        print("[retriever] ⚠️ Vectorstore not found. Creating new one...")
        return create_vector_store()

    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


def query_index(query: str, top_k: int = 3):
    """Query the vector store for relevant content."""
    vectordb = load_vector_store()
    results = vectordb.similarity_search(query, k=top_k)
    print(f"[retriever] 🔍 Retrieved {len(results)} results for query: '{query}'")
    return [doc.page_content for doc in results]
