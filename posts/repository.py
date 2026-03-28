from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, user_id: int, message_text: str) -> Message:
        db_message = Message(
            user_id=user_id, 
            message=message_text, 
            time=datetime.now(timezone.utc)
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
