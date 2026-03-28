from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, DateTime
from database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    message = Column(Text, nullable=False)
