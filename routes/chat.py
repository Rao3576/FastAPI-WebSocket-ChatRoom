from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.chat_query import ChatQueries
from datetime import datetime

router = APIRouter()
connections = {}  # room_id -> [{"socket": WebSocket, "username": str}]

# ✅ DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    username: str = Query(...),
    db: Session = Depends(get_db)
):
    await websocket.accept()

    queries = ChatQueries(db)

    # Manage connections per room
    if room_id not in connections:
        connections[room_id] = []

    # Save user socket
    connections[room_id].append({"socket": websocket, "username": username})

    # Ensure room exists in DB
    room = queries.get_room_by_room_id(room_id)
    if not room:
        room = queries.create_room(room_id, f"Room {room_id}")

    # Broadcast "user joined" message
    join_msg = {
        "username": "System",
        "content": f"⭐ {username} joined the room",
        "timestamp": datetime.now().strftime("%H:%M"),
        "system": True
    }
    for conn in connections[room_id]:
        await conn["socket"].send_json(join_msg)

    # Send previous chat history
    messages = queries.get_messages_for_room(room)
    for msg in messages:
        await websocket.send_json({
            "username": msg.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%H:%M"),
            "system": False
        })

    # Handle live messages
    try:
        while True:
            data = await websocket.receive_json()
            username = data["username"]
            content = data["content"]

            msg = queries.create_message(username, content, room)

            # Broadcast to all users
            for conn in connections[room_id]:
                await conn["socket"].send_json({
                    "username": username,
                    "content": content,
                    "timestamp": msg.timestamp.strftime("%H:%M"),
                    "system": False
                })

    except WebSocketDisconnect:
        # Remove disconnected user
        connections[room_id] = [
            c for c in connections[room_id] if c["socket"] != websocket
        ]

        # Broadcast "user left" message
        leave_msg = {
            "username": "System",
            "content": f"❌ {username} left the room",
            "timestamp": datetime.now().strftime("%H:%M"),
            "system": True
        }
        for conn in connections.get(room_id, []):
            await conn["socket"].send_json(leave_msg)


# ✅ Optional route (for simple in-memory message viewing)
@router.get("/messages")
async def fetch_messages():
    queries = ChatQueries()  # no db here
    messages = queries.get_messages()
    return {"messages": messages}











# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from repositories.chat_query import ChatQueries

# router = APIRouter()
# connections = {}  # room_id -> [websockets]

# # ✅ Dependency for DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.websocket("/ws/{room_id}")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     room_id: str,
#     username: str = Query(...),
#     db: Session = Depends(get_db)
# ):
#     await websocket.accept()

#     # Create repository object for queries
#     queries = ChatQueries(db)

#     # Manage connections
#     if room_id not in connections:
#         connections[room_id] = []
#     connections[room_id].append(websocket)

#     # Ensure room exists
#     room = queries.get_room_by_room_id(room_id)
#     if not room:
#         room = queries.create_room(room_id, f"Room {room_id}")

#     # Send previous messages
#     messages = queries.get_messages_for_room(room)
#     for msg in messages:
#         await websocket.send_json({
#             "username": msg.username,
#             "content": msg.content,
#             "timestamp": msg.timestamp.strftime("%H:%M")
#         })

#     # Handle live messages
#     try:
#         while True:
#             data = await websocket.receive_json()
#             username = data["username"]
#             content = data["content"]

#             msg = queries.create_message(username, content, room)

#             # Broadcast to all connections in the same room
#             for conn in connections[room_id]:
#                 await conn.send_json({
#                     "username": username,
#                     "content": content,
#                     "timestamp": msg.timestamp.strftime("%H:%M")
#                 })
#     except WebSocketDisconnect:
#         connections[room_id].remove(websocket)







