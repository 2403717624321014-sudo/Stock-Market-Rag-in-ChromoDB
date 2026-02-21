from vector_db_module import collection, embedding_model

def search_and_display(query):
    
    # Convert query to embedding
    query_embedding = embedding_model.encode([query])

    # Search in ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    print("\nTop Matching Results:\n")

    for i in range(len(documents)):
        print(f"Result {i+1}")
        print("Source:", metadatas[i]["source"])
        print("Date:", metadatas[i]["timestamp"])
        print("Content:")
        print(documents[i])
        print("-" * 60)


def simple_generator(question, documents):
    context = "\n".join(documents)

    return f"""
===================================================
RAG Generated Answer
===================================================

Question:
{question}

Based on retrieved financial reports:

{context}

Conclusion:
The above information represents the most relevant
market data related to your query.
"""


# -----------------------------
# TERMINAL INTERACTION
# -----------------------------
if __name__ == "__main__":

    print("📊 NIFTY 50 QUERY ENGINE STARTED")
    print("Type 'exit' to stop.\n")

    while True:
        query = input("Ask stock question: ")

        if query.lower() == "exit":
            print("Exiting Query Engine.")
            break

        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        documents = results["documents"][0]

        search_and_display(query)

        final_answer = simple_generator(query, documents)

        print(final_answer)