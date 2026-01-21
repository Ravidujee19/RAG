from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    chroma_path: str = "storage/chroma"
    chroma_collection: str = "documents"
    sqlite_path: str = "storage/memory.db"
    embedding_model: str = "all-MiniLM-L6-v2"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.1:8b"
    llm_cache_path: str = "storage/llm_cache.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
