from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatHistory
from app.services.bedrock_service import BedrockService
from app.services.rag_service import RAGService
from app.services.guardrail_service import GuardrailService
from app.dependencies import get_bedrock_service, get_rag_service, get_guardrail_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    bedrock: BedrockService = Depends(get_bedrock_service),
    rag: RAGService = Depends(get_rag_service),
    guardrail: GuardrailService = Depends(get_guardrail_service),
):
    blocked = await guardrail.check_input(request.message)
    if blocked:
        raise HTTPException(status_code=400, detail="Message blocked by content policy.")

    context_docs = await rag.retrieve(request.message, top_k=5)
    response = await bedrock.chat(
        message=request.message,
        context_docs=context_docs,
        history=request.history,
    )

    return ChatResponse(
        reply=response.content,
        sources=[doc.metadata for doc in context_docs],
        model=response.model,
    )


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    bedrock: BedrockService = Depends(get_bedrock_service),
    rag: RAGService = Depends(get_rag_service),
):
    from fastapi.responses import StreamingResponse

    context_docs = await rag.retrieve(request.message, top_k=5)

    async def event_stream():
        async for chunk in bedrock.stream_chat(request.message, context_docs, request.history):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
