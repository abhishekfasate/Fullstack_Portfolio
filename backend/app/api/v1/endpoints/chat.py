"""AI chatbot endpoint — supports both regular and SSE streaming responses."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.analytics import ChatRequest, ChatResponse
from app.services.ai_service import chat, chat_stream

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest) -> ChatResponse:
    reply, session_id = await chat(body.message, body.session_id)
    return ChatResponse(reply=reply, session_id=session_id)


@router.post("/stream")
async def chat_stream_endpoint(body: ChatRequest) -> StreamingResponse:
    """Server-Sent Events stream for real-time token delivery."""

    async def event_generator():
        session_id: str | None = None
        async for token, sid in chat_stream(body.message, body.session_id):
            session_id = sid
            yield f"data: {token}\n\n"
        # Send final event with session id so client can persist it
        yield f"event: done\ndata: {session_id}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")