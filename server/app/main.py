from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crud import chat_crud, course_crud
from routers import chat_router, course_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    chat_crud.write_llm_context_to_file()
    chat_crud.write_chat_history_to_file()
    course_crud.write_courses_to_file()


app = FastAPI(lifespan=lifespan)
app.include_router(chat_router)
app.include_router(course_router)
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
