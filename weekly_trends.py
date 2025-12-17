from datetime import datetime, timedelta
from provider_factory import get_llm_provider
from vector_store.pgvector_store import PGVectorStore
from config import PG_DSN, LLM_PROVIDER
import os


def generate_weekly_trends():
    print("📊 Generating weekly private banking trends")

    # Initialize LLM
    if LLM_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
    else:
        api_key = os.getenv("GEMINI_API_KEY")

    llm = get_llm_provider(LLM_PROVIDER, api_key)
    vector_store = PGVectorStore(PG_DSN)

    since = datetime.utcnow() - timedelta(days=7)

    # Fetch recent documents
    with vector_store.conn.cursor() as cur:
        cur.execute(
            """
            SELECT content, metadata
            FROM documents
            WHERE metadata->>'category' IS NOT NULL
            """
        )
        rows = cur.fetchall()

    documents = [row[0] for row in rows]

    if not documents:
        print("No documents found for weekly trends")
        return

    # Limit context size
    context = "\n\n".join(documents[:20])

    prompt = f"""
You are a senior private banking strategist.

Based on the following research content from the past week, identify:
1. Key investment trends
2. Asset classes gaining or losing favor
3. Macro or regulatory risks
4. Themes relevant to private banking clients

Content:
{context}

Provide a concise weekly trend summary in bullet points.
"""

    summary = llm.chat(prompt)

    print("\n===== WEEKLY PRIVATE BANKING TRENDS =====\n")
    print(summary)
