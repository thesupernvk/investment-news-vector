from llm.openai_provider import OpenAIProvider
from llm.gemini_provider import GeminiProvider

def get_llm_provider(name: str, api_key: str):
    if name == "openai":
        return OpenAIProvider(api_key)
    if name == "gemini":
        return GeminiProvider(api_key)
    raise ValueError("Unsupported provider")
