import uvicorn
from fastapi import FastAPI

from crud import chat_crud
from routers import chat_router
from schemas.json_definitions import load_schemas_into_registry
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(chat_router)
chat_crud.read_history_from_file()
load_schemas_into_registry()
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
