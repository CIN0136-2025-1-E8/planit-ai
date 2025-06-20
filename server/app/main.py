import os

import uvicorn
from fastapi import FastAPI

from core import settings
from crud import basic_chat_crud, rich_chat_crud, files_crud
from routers import basic_chat_router, rich_chat_router, files_router
from schemas.json_definitions import load_schemas_into_registry
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(files_router)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
files_crud.read_file_list_from_file()
app.include_router(basic_chat_router)
basic_chat_crud.read_history_from_file()
app.include_router(rich_chat_router)
rich_chat_crud.read_history_from_file()
load_schemas_into_registry()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique ["http://localhost:5173"]
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
