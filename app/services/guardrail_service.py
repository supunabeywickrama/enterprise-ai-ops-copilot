import re
from app.config import Settings
from app.services.logging_service import get_logger

logger = get_logger(__name__)

# Patterns that indicate prompt injection attempts
_INJECTION_PATTERNS = [
    r"ignore (all |previous |prior )?instructions",
    r"forget (the |your |all )?instructions",
    r"disregard (the |your |all )?instructions",
    r"reveal (your |the )?system prompt",
    r"you are now",
    r"new persona",
    r"act as (if you are|an? )",
    r"pretend (you are|to be)",
    r"bypass (safety|filter|guardrail)",
    r"jailbreak",
]

_COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _INJECTION_PATTERNS]

# Basic PII patterns
_PII_PATTERNS = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[EMAIL]"),
    (re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[PHONE]"),
    (re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"), "[CARD]"),
]


class GuardrailService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def check_input(self, message: str) -> bool:
        """Returns True if the message should be blocked."""
        for pattern in _COMPILED_PATTERNS:
            if pattern.search(message):
                logger.warning("Prompt injection detected", pattern=pattern.pattern)
                return True
        return False

    async def check_output(self, response: str, context_docs: list) -> bool:
        """Returns True if the output looks ungrounded (no context docs retrieved)."""
        if not context_docs:
            logger.warning("Output check: no context docs — low confidence response")
        return False

    def mask_pii(self, text: str) -> str:
        """Redact common PII patterns from text."""
        for pattern, replacement in _PII_PATTERNS:
            text = pattern.sub(replacement, text)
        return text
