from contextlib import asynccontextmanager

import firebase_admin
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials

from app.core.db import Base, engine
from app.routers import chat_router, course_router, user_router, events_router, routines_router
from app.routers import lecture_router

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(course_router, prefix="/api")
app.include_router(lecture_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(routines_router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
