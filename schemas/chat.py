from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    username: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    timestamp: datetime

    class Config:
        orm_mode = True

