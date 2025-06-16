from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, SecretStr
from typing import Optional

from schemas.json_definitions import AvailableSchemas


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    PROJECT_NAME: str = "PlanIt AI"
    DEBUG: bool = False
    DEBUG_HISTORY_FILE_PATH: Path = BASE_DIR / ".venv/history.pkl"
    DEBUG_ADVANCED_CHAT_HISTORY_FILE_PATH: Path = BASE_DIR / ".venv/advanced_chat_history.pkl"

    GOOGLE_API_KEY: Optional[SecretStr] = None
    GOOGLE_MODEL_BASIC: str = "gemma-3-27b-it"
    GOOGLE_ADVANCED_MODEL: str = "gemini-2.0-flash"

    LLM_STRUCTURED_OUTPUT_SYSTEM_INSTRUCTIONS: dict[AvailableSchemas, str] = {
        AvailableSchemas.CLASS: "You must always respond in Brazilian Portuguese. When filling properties, you must always trim white-spaces, remove line breaks, separate words that were mistakenly merged and normalize the case. Evaluations might be defined in the files together with the lessons, extract them and fill them in the proper attribute. Don't include holidays in lessons.",
        AvailableSchemas.SEMESTER: "You must always respond in Brazilian Portuguese. When filling properties, you must always trim white-spaces, remove line breaks, separate words that were mistakenly merged and normalize the case."
    }

    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()

if __name__ == "__main__":
    print("--- Configurações Carregadas ---")
    print(f"Nome do Projeto: {settings.PROJECT_NAME}")
    print(f"Modo Debug: {settings.DEBUG}")
    print(f"DEBUG - Arquivo de histórico: {settings.DEBUG_HISTORY_FILE_PATH}")
    print(f"Chave de API Google: {'Configurada' if settings.GOOGLE_API_KEY.get_secret_value() else 'NÃO CONFIGURADA'}")
    print(f"Modelo: {settings.GOOGLE_MODEL_BASIC}")

    print("\nLembre-se de criar um arquivo '.env' na pasta 'server/' com os valores reais das suas chaves e segredos!")