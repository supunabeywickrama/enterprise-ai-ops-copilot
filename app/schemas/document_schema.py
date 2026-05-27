from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentMeta(BaseModel):
    document_id: str
    filename: str
    document_type: Optional[str] = None
    chunk_count: Optional[int] = None
    ingested_at: Optional[datetime] = None


class DocumentIngestionResponse(BaseModel):
    document_id: str
    filename: str
    status: str  # queued | processing | complete | failed


class DocumentListResponse(BaseModel):
    documents: list[DocumentMeta]
    total: int
