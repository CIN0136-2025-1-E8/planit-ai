from pathlib import Path
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    PROJECT_NAME: str = "PlanIt AI"
    DEBUG: bool = False
    DEBUG_CHAT_HISTORY_FILE_PATH: Path = BASE_DIR / ".venv/chat_history.pkl"
    DEBUG_LLM_CONTEXT_FILE_PATH: Path = BASE_DIR / ".venv/llm_context.pkl"

    GOOGLE_API_KEY: Optional[SecretStr] = None
    GOOGLE_BASIC_MODEL: str = "gemma-3-27b-it"
    GOOGLE_ADVANCED_MODEL: str = "gemini-2.0-flash"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()

if __name__ == "__main__":
    print("--- Loaded Settings ---")
    print(f"Project name: {settings.PROJECT_NAME}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"DEBUG - Chat history file: {settings.DEBUG_CHAT_HISTORY_FILE_PATH}")
    print(f"DEBUG - LLM context file: {settings.DEBUG_LLM_CONTEXT_FILE_PATH}")
    print(f"Google API Key: {'Configurada' if settings.GOOGLE_API_KEY.get_secret_value() else 'NÃO CONFIGURADA'}")
    print(f"Basic LLM: {settings.GOOGLE_BASIC_MODEL}")
    print(f"Advanced LLM: {settings.GOOGLE_ADVANCED_MODEL}")
