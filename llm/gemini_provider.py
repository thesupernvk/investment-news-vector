import google.generativeai as genai
from llm.base import LLMProvider

class GeminiProvider(LLMProvider):

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")

    def embed(self, text: str):
        return genai.embed_content(
            model="models/embedding-001",
            content=text
        )["embedding"]

    def chat(self, prompt: str):
        return self.model.generate_content(prompt).text
