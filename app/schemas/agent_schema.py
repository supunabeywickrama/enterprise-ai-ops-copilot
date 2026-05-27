from pydantic import BaseModel, Field
from typing import Optional, Any


class AgentRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=4000)
    session_id: str = Field(default="default")
    metadata: Optional[dict[str, Any]] = None


class ToolCallRecord(BaseModel):
    tool: str
    input: dict[str, Any] = {}
    output: Optional[Any] = None


class AgentResponse(BaseModel):
    session_id: str
    output: str
    steps: list[str] = []
    tool_calls: list[ToolCallRecord] = []
    confidence: Optional[str] = None
    requires_human_approval: bool = False
