from vector_db_module import collection, embedding_model
from statistical_analysis_module import analyze_documents
import re


# -----------------------------------------------
# SEARCH FUNCTION
# -----------------------------------------------
def search_and_display(query):
    """Search and display results for a given query."""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )
    except Exception:
        # Fallback using embeddings
        query_embedding = embedding_model.encode([query])
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

    documents = results.get("documents", [[]])[0] if results else []
    metadatas = results.get("metadatas", [[]])[0] if results else []
    distances = results.get("distances", [[]])[0] if results else []

    if not documents:
        print("No matching documents found.")
        return [], [], []

    # Filter out results that are too dissimilar (distance > 1.5 = not relevant)
    filtered_docs, filtered_meta, filtered_dist = [], [], []
    for doc, meta, dist in zip(documents, metadatas, distances):
        if dist < 1.8:  # Only keep reasonably relevant results
            filtered_docs.append(doc)
            filtered_meta.append(meta)
            filtered_dist.append(dist)

    if not filtered_docs:
        print("No sufficiently relevant documents found for this query.")
        return [], [], []

    print("\nTop Matching Results:\n")
    for i, (doc, meta, dist) in enumerate(zip(filtered_docs, filtered_meta, filtered_dist)):
        relevance_pct = max(0, round((1 - dist / 2.0) * 100, 1))
        print(f"Result {i+1}  [Relevance: {relevance_pct}%]")
        print("Source:", meta.get("source", "Unknown"))
        print("Date:", meta.get("timestamp", "Unknown"))
        print("Content:")
        print(doc[:400] if len(doc) > 400 else doc)
        print("-" * 60)

    return filtered_docs, filtered_meta, filtered_dist


# -----------------------------------------------
# SMART ANSWER GENERATOR
# -----------------------------------------------
def simple_generator(question, documents, metadatas=None):
    """
    Generate a focused, question-specific answer from retrieved documents.
    Instead of dumping raw text, extract key facts relevant to the question.
    """
    if not documents:
        return "Sorry, I could not find relevant information to answer your question."

    question_lower = question.lower()

    # ---- Extract key facts from documents ----
    extracted_facts = []
    prices_found = []
    sources_used = []

    for i, doc in enumerate(documents):
        doc_lower = doc.lower()
        sentences = re.split(r'(?<=[.!?])\s+', doc.strip())

        for sentence in sentences:
            sent_lower = sentence.lower()
            # Check if the sentence is relevant to the question
            question_keywords = re.findall(r'\b\w{4,}\b', question_lower)
            matches = sum(1 for kw in question_keywords if kw in sent_lower)
            if matches >= 1 and len(sentence) > 30:
                extracted_facts.append(sentence.strip())

        # Extract prices / numbers from the doc
        nums = re.findall(r'Rs\s?[\d,]+(?:\.\d+)?|USD\s?[\d.]+\s?billion|[\d,]+(?:\.\d+)?%|[\d,]+(?:\.\d+)?\s(?:crore|lakh|million|billion)', doc)
        prices_found.extend(nums[:4])

        if metadatas:
            src = metadatas[i].get("source", "")
            if src:
                sources_used.append(src)

    # Deduplicate facts
    seen = set()
    unique_facts = []
    for f in extracted_facts:
        if f not in seen:
            seen.add(f)
            unique_facts.append(f)

    # Limit to top 5 most relevant facts
    top_facts = unique_facts[:5]

    # If no specific facts extracted, fall back to first 2 sentences of top document
    if not top_facts:
        fallback_sentences = re.split(r'(?<=[.!?])\s+', documents[0].strip())
        top_facts = [s.strip() for s in fallback_sentences[:3] if len(s) > 30]

    # ---- Build the answer ----
    facts_text = "\n• ".join(top_facts) if top_facts else "No specific facts extracted."
    sources_text = "\n  - ".join(set(sources_used)) if sources_used else "NIFTY Market Data"
    prices_text = ", ".join(set(prices_found[:6])) if prices_found else "See facts above"

    answer = f"""
===================================================
  RAG Answer — NIFTY 50 Stock Market System
===================================================

Question: {question}

---------------------------------------------------
Key Facts From Retrieved Documents:
---------------------------------------------------
• {facts_text}

---------------------------------------------------
Key Numbers & Prices Mentioned:
---------------------------------------------------
  {prices_text}

---------------------------------------------------
Sources Used:
---------------------------------------------------
  - {sources_text}

---------------------------------------------------
Summary:
---------------------------------------------------
Based on the retrieved market data, the question "{question}" 
relates to the above facts. The information is sourced from 
{len(documents)} relevant document(s) in the knowledge base.
===================================================
"""
    return answer


# -----------------------------------------------
# TERMINAL INTERACTION
# -----------------------------------------------
if __name__ == "__main__":
    try:
        print("[SYSTEM] NIFTY 50 QUERY ENGINE STARTED")
        print("Type 'exit' to stop.\n")
        print("Example questions you can ask:")
        print("  - What is the share price of Reliance?")
        print("  - How is HDFC Bank performing?")
        print("  - What is the NIFTY 50 index level?")
        print("  - Tell me about TCS quarterly results")
        print("  - What is the outlook for the IT sector?")
        print("  - How is SBI doing?\n")

        while True:
            try:
                query = input("Ask stock question: ").strip()

                if not query:
                    continue

                if query.lower() == "exit":
                    print("Exiting Query Engine.")
                    break

                documents, metadatas, distances = search_and_display(query)

                if not documents:
                    print("No relevant data found for this query.\n")
                    continue

                # Statistical Analysis
                analysis = analyze_documents(documents)
                print("\n[ANALYSIS] Statistical Market Analysis:\n")
                for k, v in analysis.items():
                    print(f"  {k}: {v}")

                # Generate focused answer
                final_answer = simple_generator(query, documents, metadatas)
                print(final_answer)

            except KeyboardInterrupt:
                print("\nExiting Query Engine.")
                break
            except Exception as e:
                print(f"Error processing query: {e}")
                continue

    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()