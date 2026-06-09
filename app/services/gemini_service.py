from google import genai
from app.core.config import settings

class GeminiService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def embed_text(self, text: str) -> list[float]:
        response = self.client.models.embed_content(model=settings.gemini_embedding_model, contents=text)
        vector = response.embeddings[0].values
        return [float(v) for v in vector]

    def generate_text(self, prompt: str) -> str:
        response = self.client.models.generate_content(model=settings.gemini_generation_model, contents=prompt)
        return response.text or ""

gemini_service = GeminiService()
