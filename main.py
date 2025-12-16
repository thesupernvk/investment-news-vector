from dotenv import load_dotenv
load_dotenv()

import os
from config import load_sources
from scraper.registry import SCRAPER_REGISTRY
from scraper.hn_scraper import fetch_article_content  # reused for article body
from text_chunker import chunk_text
from dedup import compute_content_hash

from provider_factory import get_llm_provider
from vector_store.pgvector_store import PGVectorStore
from config import PG_DSN, LLM_PROVIDER


# ------------------------------------------------------------------
# Banking-related categories ONLY
# ------------------------------------------------------------------

BANKING_CATEGORIES = {
    "private_banking",
    "asset_management",
    "investment_strategy",
    "regulation",
    "macroeconomics",
}


# ------------------------------------------------------------------
# Initialize providers
# ------------------------------------------------------------------

if LLM_PROVIDER == "openai":
    api_key = os.getenv("OPENAI_API_KEY")
elif LLM_PROVIDER == "gemini":
    api_key = os.getenv("GEMINI_API_KEY")
else:
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

llm = get_llm_provider(LLM_PROVIDER, api_key)
vector_store = PGVectorStore(PG_DSN)


# ------------------------------------------------------------------
# Ingestion pipeline
# ------------------------------------------------------------------

def main():
    print("🏦 Starting BANKING-ONLY ingestion pipeline")

    sources = load_sources()

    total_chunks = 0
    skipped_urls = 0
    skipped_hashes = 0
    skipped_categories = 0

    for source in sources:
        if not source.get("enabled", False):
            continue

        category = source.get("category", "").lower()

        # 🔒 FILTER NON-BANKING SOURCES
        if category not in BANKING_CATEGORIES:
            skipped_categories += 1
            continue

        source_name = source["name"]
        fetcher_name = source["fetcher"]
        article_limit = source.get("article_limit", 5)

        print(f"\n=== Processing banking source: {source_name} ({category}) ===")

        if fetcher_name not in SCRAPER_REGISTRY:
            print(f"Fetcher '{fetcher_name}' not registered, skipping.")
            continue

        fetcher = SCRAPER_REGISTRY[fetcher_name]
        articles = fetcher()[:article_limit]

        for article_index, article in enumerate(articles):
            title = article["title"]
            url = article["link"]

            # ------------------------------
            # URL deduplication
            # ------------------------------
            if vector_store.url_exists(url):
                print(f"Skipping (URL exists): {title}")
                skipped_urls += 1
                continue

            # ------------------------------
            # Fetch article content
            # ------------------------------
            content = fetch_article_content(url)
            if not content or len(content) < 500:
                print(f"Skipping (content too short): {title}")
                continue

            # ------------------------------
            # Content hash deduplication
            # ------------------------------
            content_hash = compute_content_hash(content)
            if vector_store.content_hash_exists(content_hash):
                print(f"Skipping (duplicate content): {title}")
                skipped_hashes += 1
                continue

            # ------------------------------
            # Chunking
            # ------------------------------
            chunks = chunk_text(content)
            print(f"Ingesting '{title}' → {len(chunks)} chunks")

            ids = []
            embeddings = []
            documents = []
            metadatas = []

            for chunk_index, chunk in enumerate(chunks):
                embedding = llm.embed(chunk)

                ids.append(f"{content_hash}_{chunk_index}")
                embeddings.append(embedding)
                documents.append(chunk)
                metadatas.append({
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "category": category,
                    "content_hash": content_hash,
                    "article_index": article_index,
                    "chunk_index": chunk_index,
                })

            vector_store.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            total_chunks += len(chunks)

    print("\n===== BANKING INGESTION SUMMARY =====")
    print(f"Total chunks stored: {total_chunks}")
    print(f"Skipped URLs: {skipped_urls}")
    print(f"Skipped duplicate content: {skipped_hashes}")
    print(f"Skipped non-banking sources: {skipped_categories}")
    print("✅ Banking-only PGVector ingestion completed successfully")


if __name__ == "__main__":
    main()
