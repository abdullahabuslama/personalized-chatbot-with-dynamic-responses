# main.py
from retriever import retrieve_from_query
from generator import MedicalGenerator

# ----------------- Initialize generator -----------------
generator = MedicalGenerator()
print("[INFO] Medicine RAG system ready. Type 'exit' to quit.\n")

# ----------------- Interactive query loop -----------------
while True:
    query = input("Ask a medicine question: ")
    if query.lower() in ["exit", "quit"]:
        break

    # Retrieve top 2 relevant documents from cached embeddings
    try:
        top_docs = retrieve_from_query(query, top_k=2)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print("Please run the embedding script first to generate cached embeddings.")
        continue

    if not top_docs:
        print("[INFO] No relevant documents found for this query.")
        continue

    print(f"[INFO] Retrieved {len(top_docs)} documents:")
    for i, doc in enumerate(top_docs, 1):
        print(f"Doc {i}:\n{doc}\n{'-'*30}")

    # Generate answer using retrieved documents
    answer = generator.generate(query, top_docs)

    print("\nAnswer:\n", answer)
    print("=" * 60)
