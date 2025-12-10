from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.api.routes import items
from app.core.db import engine

app = FastAPI(title="Items Service")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)

@app.on_event("startup")
def on_startup():
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)