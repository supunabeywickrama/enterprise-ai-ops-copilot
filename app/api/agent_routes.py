from fastapi import APIRouter, Depends, HTTPException
from app.schemas.agent_schema import AgentRequest, AgentResponse
from app.agents.graph import build_agent_graph
from app.agents.state import AgentState

router = APIRouter()


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    graph = build_agent_graph()
    initial_state = AgentState(
        messages=[{"role": "user", "content": request.task}],
        session_id=request.session_id,
        metadata=request.metadata or {},
    )
    try:
        result = await graph.ainvoke(initial_state)
        return AgentResponse(
            session_id=request.session_id,
            output=result["messages"][-1]["content"],
            steps=result.get("steps", []),
            tool_calls=result.get("tool_calls", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    return {"session_id": session_id, "status": "not_implemented"}
