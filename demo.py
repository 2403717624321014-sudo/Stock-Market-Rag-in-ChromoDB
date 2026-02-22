#!/usr/bin/env python3
"""
Stock Market RAG System - Live Demonstration
Shows the system in action with sample queries
"""

import sys
from vector_db_module import search_market_data
from statistical_analysis_module import analyze_documents
from query_engine import simple_generator

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def demonstrate_query(query_text, num=1):
    """Demonstrate a query and response."""
    print(f"\n[Query {num}]")
    print(f"Question: {query_text}")
    print(f"{'-'*70}")
    
    try:
        # Search
        print("Searching vector database...")
        documents = search_market_data(query_text)
        
        if not documents:
            print("   [ERROR] No documents found")
            return False
        
        print(f"   [OK] Found {len(documents)} documents")
        
        # Analyze
        print("Analyzing market data...")
        analysis = analyze_documents(documents)
        
        print("   Analysis Results:")
        for key, value in analysis.items():
            print(f"   • {key}: {value}")
        
        # Generate RAG response
        print("\nGenerating RAG response...")
        response = simple_generator(query_text, documents)
        print(response)
        
        return True
        
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False

def main():
    """Run the demonstration."""
    print(f"\n{'='*70}")
    print(f"{'STOCK MARKET RAG SYSTEM - LIVE DEMONSTRATION':^70}")
    print(f"{'='*70}")
    
    print("\nThis demonstration shows the system in action.")
    print("It performs semantic search + analysis + RAG generation.\n")
    
    # Example queries
    queries = [
        "What is the current market trend?",
        "Analyze the market volatility",
        "What is the trading signal for NIFTY?"
    ]
    
    successful = 0
    
    for i, query in enumerate(queries, 1):
        print_section(f"EXAMPLE QUERY {i}")
        if demonstrate_query(query, i):
            successful += 1
        
        if i < len(queries):
            input("\nPress Enter to continue to next query...")
    
    print_section("DEMONSTRATION SUMMARY")
    print(f"\n[SUCCESS] Successful queries: {successful}/{len(queries)}")
    print(f"\nKey Features Demonstrated:")
    print("  1. [OK] Semantic search using vector embeddings")
    print("  2. [OK] Statistical market analysis")
    print("  3. [OK] Risk assessment (volatility)")
    print("  4. [OK] Trend identification (bullish/bearish)")
    print("  5. [OK] Trading signals (buy/sell)")
    print("  6. [OK] RAG response generation")
    
    print(f"\n{'='*70}")
    print(f"{'DEMONSTRATION COMPLETE':^70}")
    print(f"{'='*70}")
    
    print("\nNext steps:")
    print("1. Try your own queries: python query_engine.py")
    print("2. Read the documentation: README.md")
    print("3. Check for errors: python test_system.py")
    print("4. Customize settings: Edit config.py")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Demonstration interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
