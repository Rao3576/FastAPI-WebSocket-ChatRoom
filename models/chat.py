from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(100), unique=True, index=True)   # ✅ Added length
    name = Column(String(100))                               # ✅ Added length
    messages = relationship("Message", back_populates="room")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))                           # ✅ Added length
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="messages")




