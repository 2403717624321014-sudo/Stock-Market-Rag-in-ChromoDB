#!/usr/bin/env python3
"""
Configuration file for Stock Market RAG System
Centralized settings for all modules
"""

import os
from pathlib import Path

# ==================== PATHS ====================
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_DB_DIR = PROJECT_ROOT / "stock_vector_db"

# Input/Output files
RAW_CORPUS_FILE = PROJECT_ROOT / "nifty_corpus.json"
PROCESSED_DATA_FILE = PROJECT_ROOT / "processed_nifty_data.json"

# ==================== DATA COLLECTION ====================
# Web sources for scraping
DATA_SOURCES = [
    "https://www.moneycontrol.com/indian-indices/nifty-50-9.html",
    "https://economictimes.indiatimes.com/markets/stocks"
]

# HTTP Headers
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Stock Market Research)"
}

# Request timeout (seconds)
REQUEST_TIMEOUT = 20

# ==================== PREPROCESSING ====================
# Text cleaning options
CLEAN_TEXT_LOWERCASE = True
CLEAN_TEXT_REMOVE_URLS = True
CLEAN_TEXT_REMOVE_SPECIAL = False  # Keep numbers for prices
CLEAN_TEXT_REMOVE_WHITESPACE = True

# Price extraction settings
PRICE_DECIMAL_PLACES = 2

# ==================== EMBEDDINGS ====================
# Sentence Transformer model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# ==================== VECTOR DATABASE ====================
# ChromaDB settings
VECTOR_DB_TYPE = "persistent"  # or "ephemeral"
COLLECTION_NAME = "nifty_market_data"

# Search parameters
DEFAULT_SEARCH_RESULTS = 3
SIMILARITY_METRIC = "cosine"

# ==================== INDICATORS ====================
# Technical indicator settings
SMA_WINDOW = 3
RSI_WINDOW = 14

# Risk thresholds
VOLATILITY_LOW = 20
VOLATILITY_MEDIUM = 50
VOLATILITY_HIGH = float('inf')

# ==================== LOGGING ====================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = PROJECT_ROOT / "system.log"
LOG_TO_CONSOLE = True

# ==================== QUERY ENGINE ====================
# Query settings
MAX_QUERY_LENGTH = 500
SHOW_FULL_DOCUMENTS = False  # Preview vs full text
DOCUMENT_PREVIEW_LENGTH = 300

# Response generation
SHOW_CONFIDENCE_SCORES = True
INCLUDE_SOURCE_ATTRIBUTION = True

# ==================== VALIDATION ====================
def validate_config():
    """Validate configuration settings."""
    try:
        # Check paths exist or can be created
        VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # Check model availability
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Check ChromaDB
        import chromadb
        
        print("✅ Configuration validated successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

# ==================== DEBUG MODE ====================
DEBUG = False  # Set to True for verbose output

if __name__ == "__main__":
    print("\n" + "="*60)
    print("STOCK MARKET RAG - CONFIGURATION")
    print("="*60)
    
    print("\n📁 PATHS:")
    print(f"  Project Root: {PROJECT_ROOT}")
    print(f"  Raw Corpus: {RAW_CORPUS_FILE}")
    print(f"  Processed Data: {PROCESSED_DATA_FILE}")
    print(f"  Vector DB: {VECTOR_DB_DIR}")
    
    print("\n🌐 DATA SOURCES:")
    for source in DATA_SOURCES:
        print(f"  • {source}")
    
    print("\n🤖 EMBEDDINGS:")
    print(f"  Model: {EMBEDDING_MODEL}")
    print(f"  Dimension: {EMBEDDING_DIMENSION}")
    
    print("\n💾 DATABASE:")
    print(f"  Type: {VECTOR_DB_TYPE}")
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Search Results: {DEFAULT_SEARCH_RESULTS}")
    
    print("\n🎯 INDICATORS:")
    print(f"  SMA Window: {SMA_WINDOW}")
    print(f"  RSI Window: {RSI_WINDOW}")
    print(f"  Risk Thresholds: Low(<{VOLATILITY_LOW}), Medium(<{VOLATILITY_MEDIUM})")
    
    print("\n" + "="*60)
    if validate_config():
        print("✨ All systems ready!")
    print("="*60 + "\n")
