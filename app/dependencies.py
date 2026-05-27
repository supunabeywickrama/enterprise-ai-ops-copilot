from fastapi import Depends

from app.config import Settings, get_settings
from app.services.bedrock_service import BedrockService
from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RAGService
from app.services.guardrail_service import GuardrailService
from app.services.evaluation_service import EvaluationService


def get_bedrock_service(settings: Settings = Depends(get_settings)) -> BedrockService:
    return BedrockService(settings)


def get_embedding_service(settings: Settings = Depends(get_settings)) -> EmbeddingService:
    return EmbeddingService(settings)


def get_rag_service(
    settings: Settings = Depends(get_settings),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> RAGService:
    return RAGService(settings, embedding_service)


def get_guardrail_service(settings: Settings = Depends(get_settings)) -> GuardrailService:
    return GuardrailService(settings)


def get_evaluation_service(
    rag_service: RAGService = Depends(get_rag_service),
) -> EvaluationService:
    return EvaluationService(rag_service)
