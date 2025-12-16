from openai import OpenAI
from llm.base import LLMProvider

class OpenAIProvider(LLMProvider):

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def embed(self, text: str):
        return self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding

    def chat(self, prompt: str):
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        ).choices[0].message.content
