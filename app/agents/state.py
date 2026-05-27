from typing import TypedDict, Any, Optional


class AgentState(TypedDict, total=False):
    messages: list[dict]
    session_id: str
    intent: str
    retrieved_docs: list
    tickets: list
    metrics: list
    draft_message: dict
    final_answer: str
    confidence: str
    requires_approval: bool
    steps: list[str]
    tool_calls: list[dict]
    metadata: dict[str, Any]
