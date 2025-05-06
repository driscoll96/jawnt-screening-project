# This file will now become the app factory for FastAPI
from fastapi import FastAPI
from .api.routes import router
from .db import init_db
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI()
    init_db()
    # Allow frontend (e.g., localhost:3000) to access backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For dev only. In prod, restrict to specific domains.
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api")
    return app

app = create_app()