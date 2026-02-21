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

collection = client.get_or_create_collection(
    name="nifty_market_data"
)


# -------------------------
# STORE DATA
# -------------------------
def store_in_chromadb(documents, embeddings, metadata):

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

    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=2
    )

    return results["documents"]


# -------------------------
# MAIN PIPELINE
# -------------------------
def build_vector_database():

    data = load_processed_data()
    documents, metadata = convert_to_documents(data)
    embeddings = generate_embeddings(documents)
    store_in_chromadb(documents, embeddings, metadata)

    print("Vector database created successfully!")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    build_vector_database()

    # Test search
    print("\nSample Query Result:")
    print(search_market_data("market trend"))

def search_stock_info(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results["documents"]