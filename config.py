import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "hn_news"

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
PG_DSN = os.getenv("PG_DSN")

SOURCES_CONFIG_PATH = BASE_DIR / "sources.yaml"

def load_sources():
    with open(SOURCES_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)["sources"]
