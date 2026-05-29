from fastapi import APIRouter, HTTPException
from app.schemas.agent_schema import AgentRequest, AgentResponse, ToolCallRecord
from app.agents.graph import build_agent_graph
from app.agents.state import AgentState

router = APIRouter()

# Build once at startup (avoid rebuilding on every request)
_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = build_agent_graph()
    return _graph


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    graph = _get_graph()
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": request.task}],
        "session_id": request.session_id,
        "metadata": request.metadata or {},
        "steps": [],
        "tool_calls": [],
        "retrieved_docs": [],
        "tickets": [],
        "metrics": [],
    }

    try:
        result = await graph.ainvoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    tool_calls = [
        ToolCallRecord(
            tool=tc.get("tool", ""),
            input=tc.get("input", {}),
            output=tc.get("output"),
        )
        for tc in result.get("tool_calls", [])
    ]

    return AgentResponse(
        session_id=request.session_id,
        output=result.get("final_answer", "No answer generated."),
        steps=result.get("steps", []),
        tool_calls=tool_calls,
        confidence=result.get("confidence"),
        requires_human_approval=result.get("requires_approval", False),
    )


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    return {"session_id": session_id, "status": "stateless — no session persistence yet"}
