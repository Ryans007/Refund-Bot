from fastapi import APIRouter, Depends, HTTPException, Form
from database.database import get_db
from models.message_model import Message
from schemes.message_scheme import MessageScheme
from graph.graph import graph
from datetime import datetime
from pydantic import BaseModel
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    thread_id: str = None
    user_message: str

@router.post("/chat/", response_model=MessageScheme)
async def create_message(
    user_message: ChatRequest,
    db=Depends(get_db)
):
    message_content = user_message.user_message.strip()
    if user_message.thread_id is not None:
        thread_id = user_message.thread_id
    else:
        thread_id = str(uuid.uuid4())
    response = graph.invoke({'user_message': message_content}, {"configurable": {"thread_id": str(thread_id)}})
    ai_message = response.get('final_answer')

    new_message = Message(
        thread_id=thread_id,
        user_message=message_content,
        ai_message=ai_message,
        create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


