import uvicorn
from fastapi import FastAPI

from crud import basic_chat_crud
from routers import basic_chat_router

app = FastAPI()
app.include_router(basic_chat_router)
basic_chat_crud.load_history_from_file()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
