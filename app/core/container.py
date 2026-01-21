from __future__ import annotations

from app.agents.aggregator import AggregatorAgent
from app.agents.local_retrieval_agent import LocalRetrievalAgent
from app.agents.registry import AgentRegistry
from app.agents.tool_agent import ToolAgent
from app.agents.web_search_agent import WebSearchAgent
from app.core.config import settings
from app.llm.cache import LLMCache
from app.llm.gemini import GeminiClient
from app.llm.ollama import OllamaClient
from app.llm.router import FallbackLLM
from app.ingest.ingestion import IngestionService
from app.memory.manager import MemoryManager
from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory
from app.rag.pipeline import RAGPipeline
from app.retrieval.indexer import Indexer
from app.retrieval.retriever import Retriever
from app.retrieval.vector_store import ChromaVectorStore


def build_orchestrator() -> AggregatorAgent:
    cache = LLMCache(settings.llm_cache_path)
    primary = GeminiClient(api_key=settings.gemini_api_key)
    fallback = OllamaClient(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
    )
    llm = FallbackLLM(primary=primary, fallback=fallback, cache=cache)
    rag = RAGPipeline(llm)

    vector_store = ChromaVectorStore(
        path=settings.chroma_path,
        collection=settings.chroma_collection,
    )
    retriever = Retriever(vector_store, model_name=settings.embedding_model)

    agents = AgentRegistry(
        [
            LocalRetrievalAgent(retriever),
            WebSearchAgent(),
            ToolAgent(),
        ]
    )
    return AggregatorAgent(llm=llm, registry=agents, rag=rag)


def build_llm_cache() -> LLMCache:
    return LLMCache(settings.llm_cache_path)


def build_ingestion_service() -> IngestionService:
    vector_store = ChromaVectorStore(
        path=settings.chroma_path,
        collection=settings.chroma_collection,
    )
    indexer = Indexer(vector_store, model_name=settings.embedding_model)
    return IngestionService(indexer)


def build_memory_manager() -> MemoryManager:
    short_term = ShortTermMemory()
    long_term = LongTermMemory(settings.sqlite_path)
    return MemoryManager(short_term, long_term)
