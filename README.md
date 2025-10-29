# FastAPI-WebSocket-ChatRoom
A **beginner-friendly real-time chat application** built with **FastAPI** and **WebSockets**.  
Users can **create/join chat rooms**, **send/receive live messages**, and **view message history** stored in the database.






---

## 🔎 What this project does (Simple)

- Lets multiple users connect to the same chat room **in real-time**.  
- When a user sends a message, **everyone else in the same room sees it instantly**.  
- Messages are **stored in a database**, so new joiners can see chat history.  
- Displays **system messages** (join / leave notifications) for all users in the room.

---

## 🧠 What is WebSocket? (Beginner explanation)

Traditional HTTP is **request → response** (client asks, server answers) — not ideal for instant updates.  
**WebSocket** creates a **persistent two-way connection** between client and server — both can send messages anytime.

### 💡 Use cases:
- Real-time chat apps  
- Live notifications / dashboards  
- Collaborative editing / multiplayer games  

In this project:
- Backend → uses **FastAPI WebSocket endpoints**  
- Frontend → uses **JavaScript WebSocket API**

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| **Backend** | FastAPI | Main framework for routes and WebSocket handling |
| **Realtime** | WebSockets | For instant, bidirectional communication |
| **Database / ORM** | SQLAlchemy + SQLite/MySQL | Store chat rooms and messages |
| **Frontend** | HTML, CSS, JavaScript | User interface and WebSocket handling |
| **Templates** | Jinja2 | For dynamic HTML pages |
| **Server (Local)** | Uvicorn | Runs the FastAPI app |

---

## 📁 Project Structure

```

FastAPI-WebSocket-ChatRoom/
│
├── main.py                      # App entrypoint: mounts templates/static and includes routes
├── database.py                  # SQLAlchemy engine & SessionLocal setup
│
├── models/
│   └── chat.py                  # SQLAlchemy models: Room, Message
│
├── repositories/
│   └── chat_query.py            # DB query class ChatQueries (create/get rooms, save/get messages)
│
├── routes/
│   └── chat.py                  # FastAPI routes + WebSocket endpoint (per-room)
│
├── templates/
│   └── chat_room.html           # HTML UI that opens WebSocket & shows messages
│
├── static/
│   ├── style.css                # CSS styling for the chat UI
│   └── js/
│       └── chat.js              # Frontend JS: connect WebSocket, send/receive messages
│
├── .gitignore
└── requirements.txt

````

---

##🔍 File-by-File Explanation

### 🧩 `main.py`
- Creates FastAPI app  
- Mounts `/static` folder (CSS/JS)  
- Loads templates folder (`templates/`)  
- Includes `routes/chat.py`  
- Runs with:
  ```bash
  uvicorn main:app --reload
````

**➡ Purpose:** Application entry point

---

### 🧩 `database.py`

* Configures SQLAlchemy engine and session
* Example (SQLite local):

  ```python
  engine = create_engine("sqlite:///./chat.db", connect_args={"check_same_thread": False})
  ```

**➡ Purpose:** Database connection configuration (SQLite/MySQL/PostgreSQL)

---

### 🧩 `models/chat.py`

Defines database tables:

```python
class Room(Base):
    id = Column(Integer, primary_key=True)
    room_id = Column(String(100), unique=True)
    name = Column(String(100))

class Message(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    content = Column(String(1000))
    timestamp = Column(DateTime, default=datetime.utcnow)
    room_id = Column(Integer, ForeignKey('rooms.id'))
```

**➡ Purpose:** Database schema for rooms and messages

---

### 🧩 `repositories/chat_query.py`

Contains reusable database query logic:

```python
def get_room_by_room_id(db, room_id)
def create_room(db, room_id, name)
def get_messages_for_room(db, room)
def create_message(db, username, content, room)
```

**➡ Purpose:** Separates DB logic from routing logic

---

### 🧩 `routes/chat.py`

Defines HTTP and WebSocket routes:

* `@router.get("/chat/{room_id}")` → renders chat UI
* `@router.websocket("/ws/{room_id}")` → manages WebSocket connections

#### WebSocket behavior:

1. Accepts connection
2. Verifies/creates room
3. Sends past messages
4. Broadcasts system message (“⭐ user joined”)
5. Handles live messages (save + broadcast)
6. On disconnect → broadcast “❌ user left”

**➡ Purpose:** Real-time chat logic

---

### 🧩 `templates/chat_room.html`

Frontend UI that:

* Lets users enter username & send messages
* Loads JS (`chat.js`) to open WebSocket
* Displays messages, history, and join/leave notifications

**➡ Purpose:** The visible chat page

---

### 🧩 `static/js/chat.js`

Frontend WebSocket logic:

```javascript
const ws = new WebSocket(`ws://${window.location.host}/ws/${roomId}?username=${username}`);
```

Handles:

* Sending messages as JSON
* Receiving and rendering messages
* Showing system messages

**➡ Purpose:** Real-time communication on the browser side

---

### 🧩 `static/style.css`

Styles chat UI:

* Message bubbles
* System message design
* Input area
* Scrollable chat container

**➡ Purpose:** Makes chat clean and readable

---

## ✅ Quick Start — Run Locally

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Create Database

```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 4️⃣ Run the Server

```bash
fastapi run main.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:8000/chat/general
```

Open same URL in another tab to simulate multiple users.

---

## 🧾 Example Chat Flow

| Step | Action                         | Description                                 |
| ---- | ------------------------------ | ------------------------------------------- |
| 1    | User opens `/chat/python`      | User connects with username (via WebSocket) |
| 2    | Server accepts connection      | Adds user to `connections[room_id]`         |
| 3    | Server loads chat history      | Sends all previous messages                 |
| 4    | Server broadcasts join message | “⭐ Ali joined the room”                     |
| 5    | User sends a message           | `{username: 'Ali', content: 'Hello!'}`      |
| 6    | Server stores message          | Saves to DB                                 |
| 7    | Server broadcasts message      | All users see message instantly             |
| 8    | User disconnects               | “❌ Ali left the room” broadcasted           |

---

## 🔐 Security & Git (Important)

### Add this in `.gitignore`

```
.env
venv/
__pycache__/
*.pyc
client_secret.json
```

### ⚠ Never commit sensitive data

If secrets were committed:

1. Remove them
2. Use `git filter-repo` to clean history
3. Rotate keys

For deployment, use **environment variables** instead of `.env` in production.

---

## 🛠 Common Errors & Fixes

| Error                                | Cause            | Fix                                                                 |
| ------------------------------------ | ---------------- | ------------------------------------------------------------------- |
| `TemplateNotFound: 'chat_room.html'` | Wrong path       | Check `templates` folder + `Jinja2Templates(directory="templates")` |
| `VARCHAR requires a length`          | MySQL            | Use `String(100)`                                                   |
| `404 /chat`                          | Route missing    | Ensure router included in `main.py`                                 |
| WebSocket not connecting             | Wrong URL        | Use correct: `ws://127.0.0.1:8000/ws/{room_id}?username=Ali`        |
| Git push blocked                     | Secrets detected | Clean git history & rotate credentials                              |

---

## 🧩 Optional Improvements

✅ Add user authentication (JWT or OAuth2)
✅ Add read receipts / message edit options
✅ Private chats
✅ Online/offline indicators
✅ Redis Pub/Sub for multi-server scaling
✅ Docker / Railway / Render deployment



---

## 👨‍💻 Author

**Muhammad Kashif Mushtaq**
