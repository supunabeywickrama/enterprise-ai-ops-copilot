from dataclasses import dataclass
from app.config import Settings
from app.services.embedding_service import EmbeddingService
from app.vector_store.chroma_store import ChromaStore
from app.services.logging_service import get_logger

logger = get_logger(__name__)


@dataclass
class RetrievedDocument:
    page_content: str
    metadata: dict
    score: float = 0.0


class Retriever:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._embedding_service = EmbeddingService(settings)
        self._store = ChromaStore(settings)

    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedDocument]:
        if self._store.count() == 0:
            logger.warning("Vector store is empty — run ingest_and_embed.py first")
            return []

        query_embedding = await self._embedding_service.embed(query)
        raw_results = self._store.query(query_embedding, top_k=top_k)

        docs = [
            RetrievedDocument(
                page_content=r["text"],
                metadata=r["metadata"],
                score=r["score"],
            )
            for r in raw_results
        ]

        logger.info("retrieval_complete", query_preview=query[:60], results=len(docs))
        return docs
