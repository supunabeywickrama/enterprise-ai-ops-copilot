"""Document ingestion orchestration — implemented in Phase 3."""
from __future__ import annotations
from app.utils.id_utils import generate_doc_id
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.embedding_service import EmbeddingService


class IngestionPipeline:
    def __init__(self, embedding_service: "EmbeddingService") -> None:
        self.embedding_service = embedding_service

    async def ingest_bytes(self, content: bytes, filename: str) -> str:
        raise NotImplementedError("IngestionPipeline.ingest_bytes — implement in Phase 3")

    async def list_documents(self) -> list[dict]:
        raise NotImplementedError("IngestionPipeline.list_documents — implement in Phase 3")

    async def delete_document(self, document_id: str) -> bool:
        raise NotImplementedError("IngestionPipeline.delete_document — implement in Phase 3")
