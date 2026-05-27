from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import Settings
    from app.services.embedding_service import EmbeddingService


class RAGService:
    """Implemented in Phase 5."""

    def __init__(self, settings: "Settings", embedding_service: "EmbeddingService") -> None:
        self.settings = settings
        self.embedding_service = embedding_service

    async def retrieve(self, query: str, top_k: int = 5) -> list:
        raise NotImplementedError("RAGService.retrieve — implement in Phase 5")
