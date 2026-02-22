# 🚀 Quick Start Guide - Stock Market RAG System

## What is this system?

A **Retrieval-Augmented Generation (RAG)** system that:
- 📊 Collects real-time NIFTY 50 stock market data
- 🔍 Searches using semantic similarity (not just keywords)
- 📈 Performs statistical analysis (volatility, trends, risk levels)
- 💡 Generates intelligent answers with market insights
- ⚡ Interactive Q&A interface

---

## ⚡ 5-Minute Setup

### 1. **Install Dependencies** (30 seconds)
```bash
pip install requests beautifulsoup4 chromadb sentence-transformers numpy
```

### 2. **Run Full Setup** (2 minutes)
```bash
cd stock-market-rag
python main.py
```

This will:
- ✅ Collect market data from web
- ✅ Process and clean the data  
- ✅ Create vector embeddings
- ✅ Build searchable database
- ✅ Generate financial indicators

### 3. **Launch Query Engine** (1 minute)
```bash
python query_engine.py
```

### 4. **Ask Questions!**
```
Ask stock question: What is the market trend?
> [Gets relevant market data]
> [Performs statistical analysis]
> [Generates RAG answer with insights]
```

---

## 🎯 Example Queries

Try these questions:

### Market Trends
```
"What is the current market trend?"
"Is the NIFTY bullish or bearish?"
"Show me the market support and resistance levels"
```

### Price Analysis
```
"What are the current stock prices?"
"Which stocks have the highest volatility?"
"What is the price range?"
```

### Risk Analysis
```
"Is the market risky right now?"
"Calculate the volatility"
"What is the risk level?"
```

### Trading Signals
```
"Should I buy or sell?"
"What is the trading recommendation?"
"What are the buy/sell signals?"
```

### Technical Analysis
```
"Calculate the simple moving average"
"What is the RSI?"
"How is the momentum?"
```

---

## 📋 Step-by-Step Manual Setup

If you want to run each step manually:

### Step 1: Collect Data
```bash
python data_collection_module.py
# Creates: nifty_corpus.json (3-5 MB)
# Time: ~10 seconds
```

### Step 2: Preprocess Data
```bash
python preprocessing_module.py  
# Creates: processed_nifty_data.json
# Time: <1 second
```

### Step 3: Analyze Indicators
```bash
python indicators_module.py
# Shows: SMA, RSI calculations
# Time: ~1 second
```

### Step 4: Build Vector Database
```bash
python vector_db_module.py
# Creates: stock_vector_db/ directory
# Time: ~5 seconds
```

### Step 5: Query System
```bash
python query_engine.py
# Interactive query interface
# Type "exit" to quit
```

---

## 🧪 Test Your Setup

```bash
python test_system.py
```

This runs 11 tests to verify:
- ✅ All imports work
- ✅ Files are in correct format
- ✅ Embeddings generate correctly
- ✅ Statistical analysis works
- ✅ Database is functional
- ✅ RAG generation works

---

## 🔍 Understanding the Output

### Search Results
```
Top Matching Results:

Result 1
Source: https://www.moneycontrol.com/...
Date: 2026-02-21
Content: [Most relevant market data]
```

### Statistical Analysis
```
📊 Statistical Market Analysis:

Mean Price: 22150.50
Max Price: 22500.00
Min Price: 21800.00
Volatility: 350.25
Risk Level: 🟡 Medium Risk
Trend: 📈 Bullish Trend
Trading Signal: ✅ BUY Recommendation
```

### RAG Response
```
===================================================
RAG Generated Answer
===================================================

Question:
What is the market trend?

Based on retrieved financial reports:
[Relevant context from database]

Conclusion:
The above information represents the most relevant
market data related to your query.
```

---

## ⚙️ Customization

### Change Embedding Model
Edit `config.py`:
```python
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
```

### Change Data Sources
Edit `config.py`:
```python
DATA_SOURCES = [
    "your-url-1",
    "your-url-2"
]
```

### Change Search Results Count
Edit `config.py`:
```python
DEFAULT_SEARCH_RESULTS = 5  # More results
```

### Change Risk Thresholds
Edit `config.py`:
```python
VOLATILITY_LOW = 50      # Adjust risk levels
VOLATILITY_MEDIUM = 100
```

---

## 🔧 Troubleshooting

### Q: "Module not found" error
**A:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Q: "Model takes long to download"
**A:** The embedding model is 80MB, downloaded once
- First run: ~1-2 minutes
- Subsequent runs: instant

### Q: "No data found" in results
**A:** 
1. Check internet connection
2. Run data collection again:
```bash
python data_collection_module.py
```

### Q: "Vector database error"
**A:** Rebuild the database:
```bash
# Delete old database
rmdir /s stock_vector_db

# Rebuild
python vector_db_module.py
```

### Q: "JSON decode error"
**A:** Data files are corrupted:
```bash
# Delete the files
del nifty_corpus.json
del processed_nifty_data.json

# Rerun data collection
python data_collection_module.py
python preprocessing_module.py
python vector_db_module.py
```

---

## 📊 System Architecture

```
┌─────────────────┐
│  Web Sources    │
│  (MoneyControl) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTML Parsing   │ ◄── data_collection_module.py
│  Text Extract   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Cleaning  │ ◄── preprocessing_module.py
│  Price Extract  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embeddings     │ ◄── sentence-transformers
│  (384-dim)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector DB      │ ◄── ChromaDB
│  (Similarity)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  User Query     │ ◄── query_engine.py
│  Embedding      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Semantic       │
│  Search         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Retrieved      │ ◄── statistical_analysis_module.py
│  Documents      │
│  + Analysis     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG Response   │ ◄── simple_generator()
│  Generation     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Answer to      │
│  User           │
└─────────────────┘
```

---

## 📚 Files Overview

| File | Purpose | Input | Output |
|------|---------|-------|--------|
| `data_collection_module.py` | Web scraping | URLs | `nifty_corpus.json` |
| `preprocessing_module.py` | Data cleaning | `nifty_corpus.json` | `processed_nifty_data.json` |
| `vector_db_module.py` | Embedding & DB | `processed_nifty_data.json` | `stock_vector_db/` |
| `query_engine.py` | Interactive Q&A | User input | Analysis + Answer |
| `statistical_analysis_module.py` | Market analysis | Documents | Metrics |
| `indicators_module.py` | Technical analysis | Prices | SMA, RSI |
| `config.py` | Settings | - | Configuration |
| `test_system.py` | Testing | - | Test results |

---

## 💡 Tips for Best Results

1. **Be Specific**: "NIFTY 50 bullish trend" > "market"
2. **Use Terms**: "volatility", "resistance", "momentum"
3. **Ask Clearly**: "What is the risk level?" > "Risk?"
4. **Check Trends**: Market trends appear every day

---

## 🎓 Learning Outcomes

After using this system, you'll understand:
- ✅ How RAG systems work
- ✅ Vector embeddings and similarity search
- ✅ ChromaDB usage
- ✅ Data pipelines
- ✅ Financial analysis
- ✅ Python best practices

---

## 📞 Need Help?

1. **Check README.md** for full documentation
2. **Run test_system.py** to diagnose issues
3. **Check config.py** for customization options
4. **Review module docstrings** for technical details

---

## ✨ You're Ready!

```bash
# One command to rule them all:
python main.py && python query_engine.py
```

**Start exploring the market with AI! 🚀**

---

**Happy Analyzing!** 📈
