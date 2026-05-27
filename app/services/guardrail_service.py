from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import Settings


class GuardrailService:
    """Implemented in Phase 6."""

    def __init__(self, settings: "Settings") -> None:
        self.settings = settings

    async def check_input(self, message: str) -> bool:
        """Returns True if the message should be blocked."""
        raise NotImplementedError("GuardrailService.check_input — implement in Phase 6")

    async def check_output(self, response: str, context_docs: list) -> bool:
        raise NotImplementedError("GuardrailService.check_output — implement in Phase 6")

    def mask_pii(self, text: str) -> str:
        raise NotImplementedError("GuardrailService.mask_pii — implement in Phase 6")
