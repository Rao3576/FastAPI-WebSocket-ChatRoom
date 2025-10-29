from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_routes

app = FastAPI(title="FastAPI Chat Room")

# Mount static folder (for CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template folder
templates = Jinja2Templates(directory="templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routes)
# ------------------------------
# ROUTE TO RENDER CHAT ROOM PAGE
# ------------------------------
@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat_room.html", {"request": request})


# ------------------------------
# SIMPLE WEBSOCKET CHAT ENDPOINT
# ------------------------------
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            for conn in connections:
                if conn != websocket:
                    await conn.send_json(data)
    except Exception:
        connections.remove(websocket)

# @app.get("/")
# async def home(request: Request):
#     return templates.TemplateResponse("chat_room.html", {"request": request})
