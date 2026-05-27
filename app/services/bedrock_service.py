from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import Settings


@dataclass
class BedrockResponse:
    content: str
    model: str


class BedrockService:
    """Implemented in Phase 2."""

    def __init__(self, settings: "Settings") -> None:
        self.settings = settings

    async def chat(self, message: str, context_docs: list, history: list) -> BedrockResponse:
        raise NotImplementedError("BedrockService.chat — implement in Phase 2")

    async def stream_chat(self, message: str, context_docs: list, history: list):
        raise NotImplementedError("BedrockService.stream_chat — implement in Phase 2")
        yield  # make this a generator
