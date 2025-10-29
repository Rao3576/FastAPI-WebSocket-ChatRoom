from sqlalchemy.orm import Session
from models.chat import Room, Message
from datetime import datetime

# simple in-memory fallback store
chat_history = []

class ChatQueries:
    """All DB queries related to chat (rooms & messages)."""

    def __init__(self, db: Session = None):
        self.db = db

    # ✅ Get room by room_id
    def get_room_by_room_id(self, room_id: str):
        if not self.db:
            return None
        return self.db.query(Room).filter(Room.room_id == room_id).first()

    # ✅ Create new room
    def create_room(self, room_id: str, name: str):
        if not self.db:
            return None
        new_room = Room(room_id=room_id, name=name)
        self.db.add(new_room)
        self.db.commit()
        self.db.refresh(new_room)
        return new_room

    # ✅ Get all messages for a room
    def get_messages_for_room(self, room: Room):
        if not self.db:
            return []
        return (
            self.db.query(Message)
            .filter(Message.room_id == room.id)
            .order_by(Message.timestamp.asc())
            .all()
        )

    # ✅ Save a new DB message
    def create_message(self, username: str, content: str, room: Room):
        if not self.db:
            return None
        new_message = Message(
            username=username,
            content=content,
            room_id=room.id,
            timestamp=datetime.now()
        )
        self.db.add(new_message)
        self.db.commit()
        self.db.refresh(new_message)
        return new_message

    # ✅ In-memory helper methods (for testing or temporary storage)
    def save_message(self, message: str, timestamp: str):
        chat_history.append({"message": message, "time": timestamp})

    def get_messages(self):
        return chat_history











# from sqlalchemy.orm import Session
# from models.chat import Room, Message
# from datetime import datetime

# class ChatQueries:
#     """All DB queries related to chat (rooms & messages)."""

#     def __init__(self, db: Session):
#         self.db = db

#     # ✅ Get room by room_id
#     def get_room_by_room_id(self, room_id: str):
#         return self.db.query(Room).filter(Room.room_id == room_id).first()

#     # ✅ Create new room
#     def create_room(self, room_id: str, name: str):
#         new_room = Room(room_id=room_id, name=name)
#         self.db.add(new_room)
#         self.db.commit()
#         self.db.refresh(new_room)
#         return new_room

#     # ✅ Get all messages for a room
#     def get_messages_for_room(self, room: Room):
#         return (
#             self.db.query(Message)
#             .filter(Message.room_id == room.id)
#             .order_by(Message.timestamp.asc())
#             .all()
#         )

#     # ✅ Save a new message
#     def create_message(self, username: str, content: str, room: Room):
#         new_message = Message(
#             username=username,
#             content=content,
#             room_id=room.id,
#             timestamp=datetime.now()
#         )
#         self.db.add(new_message)
#         self.db.commit()
#         self.db.refresh(new_message)
#         return new_message
  