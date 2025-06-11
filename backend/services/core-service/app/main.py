# app/main.py
from fastapi import FastAPI
from app.core.db.database import Base, engine
from app.api.routes import book_route

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(book_route.router)
    Base.metadata.create_all(bind=engine)
    return app

app = create_app()  # ساخت اپلیکیشن
