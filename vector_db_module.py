import json
import chromadb
from sentence_transformers import SentenceTransformer


# -------------------------
# LOAD PROCESSED DATA
# -------------------------
def load_processed_data(file_path="processed_nifty_data.json"):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


# -------------------------
# CONVERT DATA TO DOCUMENTS
# -------------------------
def convert_to_documents(data):

    documents = []
    metadata = []

    for entry in data:

        doc = f"""
        Stock Market Report
        Source: {entry['source']}
        Date: {entry['timestamp']}
        Market News: {entry['clean_text']}
        Price Values: {entry['clean_prices']}
        """

        documents.append(doc)

        metadata.append({
            "source": entry["source"],
            "timestamp": entry["timestamp"]
        })

    return documents, metadata


# -------------------------
# EMBEDDING MODEL
# -------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(documents):
    return embedding_model.encode(documents)


# -------------------------
# CHROMA DATABASE SETUP
# -------------------------
client = chromadb.PersistentClient(path="./stock_vector_db")

# Get or create the collection (used for querying)
collection = client.get_or_create_collection(
    name="nifty_market_data"
)


# -------------------------
# STORE DATA
# -------------------------
def store_in_chromadb(documents, embeddings, metadata):
    """Store documents - clears existing data first to avoid duplicates."""
    existing_count = collection.count()
    if existing_count > 0:
        # Delete all existing IDs to start fresh
        existing_ids = collection.get()["ids"]
        if existing_ids:
            collection.delete(ids=existing_ids)
        print(f"Cleared {existing_count} old documents from vector database.")

    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadata,
        ids=[str(i) for i in range(len(documents))]
    )


# -------------------------
# SEARCH FUNCTION
# -------------------------
def search_market_data(query):
    """Search market data using a query string."""
    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=2
    )

    # Return flattened list of documents
    return results.get("documents", [[]])[0] if results else []


# -------------------------
# MAIN PIPELINE
# -------------------------
def build_vector_database():

    data = load_processed_data()
    documents, metadata = convert_to_documents(data)
    embeddings = generate_embeddings(documents)
    store_in_chromadb(documents, embeddings, metadata)

    print("Vector database created successfully!")


def search_stock_info(query):
    """Search for stock information using the query."""
    query_embedding = embedding_model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=2
    )
    return results.get("documents", [[]])[0] if results else []


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    build_vector_database()

    # Test search
    print("\nSample Query Result:")
    results = search_market_data("market trend")
    for doc in results:
        print(doc[:200] + "...")