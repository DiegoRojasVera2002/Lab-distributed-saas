from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

# El archivo se guarda dentro del contenedor en /data
DB_FILE = Path("/data/chat.db")
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
