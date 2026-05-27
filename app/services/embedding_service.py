from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import Settings


class EmbeddingService:
    """Implemented in Phase 4."""

    def __init__(self, settings: "Settings") -> None:
        self.settings = settings

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("EmbeddingService.embed — implement in Phase 4")

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("EmbeddingService.embed_batch — implement in Phase 4")
