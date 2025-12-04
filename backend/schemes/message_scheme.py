from typing import Optional
from pydantic import BaseModel

class MessageScheme(BaseModel):
    """Estrutura de dados para mensagens trocadas em um thread."""
    thread_id: str
    user_message: str
    ai_message: Optional[str] = None
    create_at: str