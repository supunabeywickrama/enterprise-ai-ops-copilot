from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.rag_service import RAGService
    from app.schemas.evaluation_schema import EvaluationRequest, EvaluationResponse


class EvaluationService:
    """Implemented in Phase 11."""

    def __init__(self, rag_service: "RAGService") -> None:
        self.rag_service = rag_service

    async def evaluate_single(self, request: "EvaluationRequest") -> "EvaluationResponse":
        raise NotImplementedError("EvaluationService.evaluate_single — implement in Phase 11")

    async def evaluate_batch(self, requests: list) -> list:
        raise NotImplementedError("EvaluationService.evaluate_batch — implement in Phase 11")

    async def generate_report(self) -> dict:
        raise NotImplementedError("EvaluationService.generate_report — implement in Phase 11")
