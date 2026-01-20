from app.core.config import settings
from app.llm.gemini import GeminiClient


def get_gemini_client() -> GeminiClient:
    return GeminiClient(api_key=settings.gemini_api_key)
