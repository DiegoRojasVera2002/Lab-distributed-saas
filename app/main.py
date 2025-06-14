from fastapi import FastAPI, WebSocket, Depends
from sqlmodel import select, Session
from .database import init_db, get_session
from .models import Message

app = FastAPI(
    title="Chat-as-a-Service (SaaS Demo)",
    version="0.1.0",
    description="Ejemplo de laboratorio de Sistemas Distribuidos: REST + WebSocket sobre FastAPI."
)

# ---------- DB init ----------
@app.on_event("startup")
def on_startup():
    init_db()

# ---------- REST ----------
@app.post("/messages", status_code=201)
def create_message(msg: Message, session: Session = Depends(get_session)):
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg

@app.get("/messages")
def get_messages(limit: int = 50, session: Session = Depends(get_session)):
    stmt = select(Message).order_by(Message.created_at.desc()).limit(limit)
    return session.exec(stmt).all()

# ---------- WebSocket broadcasting ----------
active_clients: set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_clients.add(ws)
    try:
        while True:
            data = await ws.receive_text()
            for client in active_clients:
                if client is not ws:
                    await client.send_text(data)
    except Exception:
        # Cliente cerró conexión
        pass
    finally:
        active_clients.remove(ws)
