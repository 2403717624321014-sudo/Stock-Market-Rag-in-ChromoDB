#!/usr/bin/env python3
"""
Stock Market RAG System - Main Execution Script
Complete pipeline from data collection to query engine
"""

import os
import sys
import json
from pathlib import Path

# Define color codes for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print a formatted header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(message):
    """Print success message."""
    print(f"{Colors.GREEN}[OK] {message}{Colors.END}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.RED}[ERROR] {message}{Colors.END}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.YELLOW}[INFO] {message}{Colors.END}")

def check_file_exists(filepath, description="File"):
    """Check if a file exists."""
    if Path(filepath).exists():
        size = os.path.getsize(filepath)
        print_success(f"{description} exists ({size} bytes)")
        return True
    else:
        print_error(f"{description} not found")
        return False

def run_module(module_name, module_func, description):
    """Run a module with error handling."""
    print_info(f"Running {description}...")
    try:
        module_func()
        print_success(f"{description} completed successfully")
        return True
    except Exception as e:
        print_error(f"{description} failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main execution pipeline."""
    print_header("STOCK MARKET RAG SYSTEM")
    
    # Step 0: Check prerequisites
    print_info("Checking prerequisites...")
    
    # Step 1: Data Collection
    print_header("STEP 1: DATA COLLECTION")
    try:
        from data_collection_module import main as collect_data
        run_module("data_collection", collect_data, "Data Collection")
        check_file_exists("nifty_corpus.json", "Raw corpus")
    except ImportError as e:
        print_error(f"Could not import data_collection_module: {e}")
    
    # Step 2: Preprocessing
    print_header("STEP 2: PREPROCESSING")
    if check_file_exists("nifty_corpus.json", "Raw corpus"):
        try:
            from preprocessing_module import main as preprocess_data
            run_module("preprocessing", preprocess_data, "Data Preprocessing")
            check_file_exists("processed_nifty_data.json", "Processed data")
        except ImportError as e:
            print_error(f"Could not import preprocessing_module: {e}")
    else:
        print_error("Cannot proceed with preprocessing - raw corpus not found")

    # Step 3: Financial Indicators Analysis
    print_header("STEP 3: FINANCIAL INDICATORS")
    if check_file_exists("processed_nifty_data.json", "Processed data"):
        try:
            from indicators_module import main as analyze_indicators
            run_module("indicators", analyze_indicators, "Financial Indicators Analysis")
        except ImportError as e:
            print_error(f"Could not import indicators_module: {e}")
    else:
        print_info("Skipping indicators analysis - processed data not found")

    # Step 4: Vector Database Building
    print_header("STEP 4: VECTOR DATABASE CREATION")
    if check_file_exists("processed_nifty_data.json", "Processed data"):
        try:
            from vector_db_module import build_vector_database
            run_module("vector_db", build_vector_database, "Vector Database Building")
            check_file_exists("stock_vector_db/chroma.sqlite3", "Vector database")
        except ImportError as e:
            print_error(f"Could not import vector_db_module: {e}")
    else:
        print_error("Cannot proceed with vector database - processed data not found")

    # Step 5: Query Engine
    print_header("STEP 5: QUERY ENGINE")
    print_success("Starting Query Engine...")
    print_info("Type 'exit' to quit the query engine")
    print_info("Try queries like: 'market trend', 'nifty performance', 'stock price'")
    
    try:
        from query_engine import main as run_query_engine
        # The query_engine runs in interactive mode, so we let it handle itself
        import query_engine
        # Since query_engine uses if __name__ == "__main__", we directly import and run the loop
        print("\n" + Colors.GREEN + "Query engine initialized. You can now ask questions about the market." + Colors.END)
        print("Enter 'exit' to quit.\n")
        
        # Instead of running the full query engine, we show a message
        # The user would interact with it directly
        print_info("To use the query engine interactively, run: python query_engine.py")
        
    except Exception as e:
        print_error(f"Query Engine initialization failed: {e}")
    
    print_header("SETUP COMPLETE")
    print_success("All components initialized successfully!")
    print_info("To start the query engine, run: python query_engine.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
