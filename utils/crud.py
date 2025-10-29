# from sqlalchemy.orm import Session
# from models.chat import Room, Message
# from datetime import datetime

# # ✅ Get room by room_id
# def get_room_by_room_id(db: Session, room_id: str):
#     return db.query(Room).filter(Room.room_id == room_id).first()

# # ✅ Create new room
# def create_room(db: Session, room_id: str, name: str):
#     new_room = Room(room_id=room_id, name=name)
#     db.add(new_room)
#     db.commit()
#     db.refresh(new_room)
#     return new_room

# # ✅ Get all messages of a specific room
# def get_messages_for_room(db: Session, room: Room):
#     return (
#         db.query(Message)
#         .filter(Message.room_id == room.id)
#         .order_by(Message.timestamp.asc())
#         .all()
#     )

# # ✅ Create and save a message with timestamp
# def create_message(db: Session, username: str, content: str, room: Room):
#     new_message = Message(
#         username=username,
#         content=content,
#         room_id=room.id,
#         timestamp=datetime.now()  # 🕒 Save message time
#     )
#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)
#     return new_message
