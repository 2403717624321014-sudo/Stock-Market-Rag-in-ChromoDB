#!/usr/bin/env python3
"""
Stock Market RAG System - FastAPI Backend
Bridges the query engine to the web UI.
"""

import os
import sys

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import re

# -----------------------------------------------
# LAZY-LOAD HEAVY MODULES (avoids slow startup)
# -----------------------------------------------
_collection = None
_embedding_model = None


def get_collection_and_model():
    global _collection, _embedding_model
    if _collection is None or _embedding_model is None:
        from vector_db_module import collection, embedding_model
        _collection = collection
        _embedding_model = embedding_model
    return _collection, _embedding_model


# -----------------------------------------------
# FASTAPI APP
# -----------------------------------------------
app = FastAPI(
    title="Stock Market RAG API",
    description="NIFTY 50 Retrieval-Augmented Generation Query System",
    version="1.0.0"
)

# Mount the frontend static directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# -----------------------------------------------
# MODELS
# -----------------------------------------------
class QueryRequest(BaseModel):
    query: str
    n_results: Optional[int] = 3


class QueryResult(BaseModel):
    content: str
    source: str
    date: str
    relevance: float


class AnalysisResult(BaseModel):
    mean_price: Optional[float] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    volatility: Optional[float] = None
    risk_level: str = "Unknown"
    trend: str = "Unknown"
    trading_signal: str = "Unknown"
    status: Optional[str] = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    results: list[QueryResult]
    analysis: AnalysisResult
    doc_count: int


# -----------------------------------------------
# HELPER FUNCTIONS (adapted from query_engine.py)
# -----------------------------------------------
def search_documents(query: str, n_results: int = 3):
    collection, embedding_model = get_collection_and_model()
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
    except Exception:
        query_embedding = embedding_model.encode([query])
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

    documents = results.get("documents", [[]])[0] if results else []
    metadatas = results.get("metadatas", [[]])[0] if results else []
    distances = results.get("distances", [[]])[0] if results else []

    filtered_docs, filtered_meta, filtered_dist = [], [], []
    for doc, meta, dist in zip(documents, metadatas, distances):
        if dist < 1.8:
            filtered_docs.append(doc)
            filtered_meta.append(meta)
            filtered_dist.append(dist)

    return filtered_docs, filtered_meta, filtered_dist


def generate_answer(question: str, documents: list, metadatas: list = None) -> str:
    if not documents:
        return "Sorry, I could not find relevant information to answer your question."

    question_lower = question.lower()
    extracted_facts = []
    sources_used = []

    for i, doc in enumerate(documents):
        sentences = re.split(r'(?<=[.!?])\s+', doc.strip())
        for sentence in sentences:
            sent_lower = sentence.lower()
            question_keywords = re.findall(r'\b\w{4,}\b', question_lower)
            matches = sum(1 for kw in question_keywords if kw in sent_lower)
            if matches >= 1 and len(sentence) > 30:
                extracted_facts.append(sentence.strip())

        if metadatas:
            src = metadatas[i].get("source", "")
            if src:
                sources_used.append(src)

    seen = set()
    unique_facts = []
    for f in extracted_facts:
        if f not in seen:
            seen.add(f)
            unique_facts.append(f)
    top_facts = unique_facts[:5]

    if not top_facts:
        fallback_sentences = re.split(r'(?<=[.!?])\s+', documents[0].strip())
        top_facts = [s.strip() for s in fallback_sentences[:3] if len(s) > 30]

    if not top_facts:
        return "I found some relevant documents but could not extract specific facts. Please try rephrasing your question."

    answer_lines = []
    for fact in top_facts:
        answer_lines.append(f"• {fact}")

    sources_note = ""
    if sources_used:
        unique_sources = list(set(sources_used))
        sources_note = f"\n\n**Sources:** {', '.join(unique_sources)}"

    return "\n".join(answer_lines) + sources_note


def run_statistical_analysis(documents: list) -> AnalysisResult:
    from statistical_analysis_module import analyze_documents
    raw = analyze_documents(documents)

    if "Status" in raw:
        return AnalysisResult(status=raw["Status"])

    return AnalysisResult(
        mean_price=raw.get("Mean Price"),
        max_price=raw.get("Max Price"),
        min_price=raw.get("Min Price"),
        volatility=raw.get("Volatility"),
        risk_level=raw.get("Risk Level", "Unknown"),
        trend=raw.get("Trend", "Unknown"),
        trading_signal=raw.get("Trading Signal", "Unknown")
    )


# -----------------------------------------------
# ROUTES
# -----------------------------------------------
@app.get("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Stock Market RAG API is running. Frontend not found."}


@app.get("/health")
def health_check():
    try:
        collection, _ = get_collection_and_model()
        doc_count = collection.count()
        return {
            "status": "healthy",
            "vector_db": "connected",
            "documents_indexed": doc_count
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }


@app.post("/query", response_model=QueryResponse)
def query_stocks(request: QueryRequest):
    if not request.query or len(request.query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query must be at least 3 characters long.")
    if len(request.query) > 500:
        raise HTTPException(status_code=400, detail="Query is too long (max 500 chars).")

    try:
        docs, metas, dists = search_documents(request.query, request.n_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

    if not docs:
        return QueryResponse(
            question=request.query,
            answer="No relevant documents found for your query. Try different keywords related to NIFTY 50 stocks.",
            results=[],
            analysis=AnalysisResult(status="No data available"),
            doc_count=0
        )

    # Build result list
    results = []
    for doc, meta, dist in zip(docs, metas, dists):
        relevance_pct = max(0.0, round((1 - dist / 2.0) * 100, 1))
        content_preview = doc[:500].strip() if len(doc) > 500 else doc.strip()
        results.append(QueryResult(
            content=content_preview,
            source=meta.get("source", "NIFTY Market Data"),
            date=meta.get("timestamp", "Unknown"),
            relevance=relevance_pct
        ))

    # Generate answer
    answer = generate_answer(request.query, docs, metas)

    # Statistical analysis
    analysis = run_statistical_analysis(docs)

    return QueryResponse(
        question=request.query,
        answer=answer,
        results=results,
        analysis=analysis,
        doc_count=len(docs)
    )


# -----------------------------------------------
# RUN
# -----------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
