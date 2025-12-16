from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os

from provider_factory import get_llm_provider
from vector_store.pgvector_store import PGVectorStore
from config import PG_DSN, LLM_PROVIDER


# ------------------------------------------------------------------
# App setup
# ------------------------------------------------------------------

app = FastAPI(title="RAG Chatbot (PGVector + Multi-LLM)")


# ------------------------------------------------------------------
# Initialize providers (swappable)
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
# Request / Response models
# ------------------------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5


class Source(BaseModel):
    title: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]


# ------------------------------------------------------------------
# Prompt builder
# ------------------------------------------------------------------

def build_prompt(question: str, contexts: List[str]) -> str:
    joined_context = "\n\n---\n\n".join(contexts)

    return f"""
You are a helpful assistant.
Answer the question ONLY using the context below.
If the answer cannot be found in the context, say:
"I don't know based on the available data."

Context:
{joined_context}

Question:
{question}

Answer:
""".strip()


# ------------------------------------------------------------------
# API endpoint
# ------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # 1. Embed user query
    query_embedding = llm.embed(request.question)

    # 2. Vector similarity search
    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        k=request.top_k
    )

    if not results:
        return ChatResponse(
            answer="I don't know based on the available data.",
            sources=[]
        )

    documents = []
    metadatas = []

    for content, metadata in results:
        documents.append(content)
        metadatas.append(metadata)

    # 3. Build LLM prompt
    prompt = build_prompt(request.question, documents)

    # 4. Generate answer
    answer = llm.chat(prompt).strip()

    # 5. Collect unique sources
    seen = set()
    sources = []

    for meta in metadatas:
        key = (meta.get("title"), meta.get("url"))
        if key not in seen:
            sources.append(
                Source(
                    title=meta.get("title", ""),
                    url=meta.get("url", "")
                )
            )
            seen.add(key)

    return ChatResponse(
        answer=answer,
        sources=sources
    )
