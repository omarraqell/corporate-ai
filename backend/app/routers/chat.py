import uuid

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.conversation import Conversation
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.orchestrator import OrchestratorService

router = APIRouter(tags=["chat"])

orchestrator = OrchestratorService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """Main chat endpoint. Runs the full orchestration pipeline."""
    result = await orchestrator.handle_message(
        db=db,
        user_id=request.user_id,
        session_id=request.session_id,
        message=request.message,
    )
    return ChatResponse(
        message=result["message"],
        session_id=result["session_id"],
        classification=result["classification"],
        agent_name=", ".join(result["agents_used"]),
    )


@router.get("/conversations/{user_id}")
async def get_conversations(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get all conversation sessions for a user."""
    result = await db.execute(
        select(Conversation.session_id)
        .where(Conversation.user_id == user_id)
        .distinct()
        .order_by(Conversation.session_id)
    )
    session_ids = [row[0] for row in result.all()]
    return {"user_id": user_id, "sessions": session_ids}


@router.get("/conversations/{user_id}/{session_id}")
async def get_conversation_history(
    user_id: str,
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get full conversation history for a session."""
    result = await db.execute(
        select(Conversation)
        .where(
            Conversation.user_id == user_id,
            Conversation.session_id == session_id,
        )
        .order_by(Conversation.created_at)
    )
    messages = result.scalars().all()
    return {
        "session_id": session_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "agent_name": msg.agent_name,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ],
    }


@router.websocket("/ws/chat/{session_id}")
async def chat_websocket(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat.
    Sends intermediate status updates as agents work.
    """
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            user_id = data.get("user_id", "anonymous")
            message = data.get("message", "")

            if not message:
                await websocket.send_json({"type": "error", "content": "Empty message"})
                continue

            # Send status: classifying
            await websocket.send_json({
                "type": "status",
                "content": "Classifying your request...",
            })

            # Get a fresh DB session for the websocket
            from app.database import async_session
            async with async_session() as db:
                result = await orchestrator.handle_message(
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    message=message,
                )

            # Send final response
            await websocket.send_json({
                "type": "message",
                "content": result["message"],
                "classification": result["classification"],
                "agents_used": result["agents_used"],
            })

    except WebSocketDisconnect:
        pass
