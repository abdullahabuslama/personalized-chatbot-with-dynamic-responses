# retriever.py
import os
import pickle
import numpy as np

# Paths to cached files
EMBEDDINGS_FILE = r"C:\Mohamed\rag opensource (1)\New folder\simple_rag\doc_embeddings.npy"
DOCS_FILE = r"C:\Mohamed\rag opensource (1)\New folder\simple_rag\documents.pkl"

def load_cached_embeddings():
    """Load cached documents and embeddings"""
    if not os.path.exists(EMBEDDINGS_FILE) or not os.path.exists(DOCS_FILE):
        raise FileNotFoundError(
            "Cached embeddings/documents not found. Run the embedding script first."
        )
    embeddings = np.load(EMBEDDINGS_FILE)
    with open(DOCS_FILE, "rb") as f:
        documents = pickle.load(f)
    print(f"[INFO] Loaded {len(documents)} documents and embeddings from cache.")
    return documents, embeddings

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query_embedding, documents, embeddings, top_k=3):
    """
    Retrieve top_k most relevant documents based on query embedding
    
    Args:
        query_embedding: np.array vector for the query
        documents: list of documents
        embeddings: np.array of precomputed document embeddings
        top_k: number of top documents to return
    """
    sims = [cosine_similarity(query_embedding, doc_emb) for doc_emb in embeddings]
    top_idx = np.argsort(sims)[-top_k:][::-1]
    top_docs = [documents[i] for i in top_idx]
    print(f"[INFO] Retrieved top {top_k} documents.")
    return top_docs

# Optional: small wrapper if using local embedding model like SentenceTransformer
from sentence_transformers import SentenceTransformer

# Load your embedding model (same one used to generate embeddings)
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_from_query(query, top_k=3):
    """Load cached embeddings, embed query, and retrieve top-k documents"""
    documents, embeddings = load_cached_embeddings()
    print("[INFO] Embedding query...")
    query_emb = model.encode(query)
    print("[INFO] Query embedding done.")
    return retrieve(query_emb, documents, embeddings, top_k=top_k)
