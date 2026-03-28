from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import MessageCreate
from repository import MessageRepository
from security import get_current_user_id

app = FastAPI(title="Posts Microservice")

@app.post("/message", status_code=status.HTTP_201_CREATED)
def create_message(
    msg: MessageCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = MessageRepository(db)
    repo.create_message(user_id=user_id, message_text=msg.message)
    
    return None
