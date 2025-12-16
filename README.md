# Banking Insights RAG Pipeline

A Python-based system that scrapes publicly available investment and wealth-management insights from trusted financial websites, embeds the content, and stores it in a vector database to power a retrieval-augmented chat application.

## Features
- Banking-focused web scraping (UBS, BlackRock)
- robots.txt–compliant ingestion
- Chunking and deduplication
- PGVector-backed vector storage
- Swappable LLM providers (OpenAI, Gemini)
- FastAPI-based RAG chatbot

## Tech Stack
- Python 3.11+
- PostgreSQL + pgvector
- FastAPI
- OpenAI / Gemini
- BeautifulSoup
- APScheduler

## Setup (Local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Run ingestion
```bash
python main.py
```
## Run RAG API
```bash
uvicorn rag_api:app --reload
```
