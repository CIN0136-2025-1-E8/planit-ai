from pathlib import Path
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from schemas.json_definitions import AvailableSchemas


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    PROJECT_NAME: str = "PlanIt AI"
    DEBUG: bool = False
    DEBUG_BASIC_CHAT_HISTORY_FILE_PATH: Path = BASE_DIR / ".venv/basic_chat_history.pkl"

    GOOGLE_API_KEY: Optional[SecretStr] = None
    GOOGLE_BASIC_MODEL: str = "gemma-3-27b-it"
    GOOGLE_ADVANCED_MODEL: str = "gemini-2.0-flash"

    LLM_STRUCTURED_OUTPUT_SYSTEM_INSTRUCTIONS: dict[AvailableSchemas, str] = {
        AvailableSchemas.CLASS: "You must always respond in Brazilian Portuguese. When filling properties, you must always trim white-spaces, remove line breaks, separate words that were mistakenly merged and normalize the case. Evaluations might be defined in the files together with the lessons, extract them and fill them in the proper attribute. Don't include holidays in lessons.",
        AvailableSchemas.SEMESTER: "You must always respond in Brazilian Portuguese. When filling properties, you must always trim white-spaces, remove line breaks, separate words that were mistakenly merged and normalize the case."
    }

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
    print(f"DEBUG - History file for basic chat: {settings.DEBUG_BASIC_CHAT_HISTORY_FILE_PATH}")
    print(f"Google API Key: {'Configurada' if settings.GOOGLE_API_KEY.get_secret_value() else 'NÃO CONFIGURADA'}")
    print(f"Basic LLM: {settings.GOOGLE_BASIC_MODEL}")
    print(f"Advanced LLM: {settings.GOOGLE_ADVANCED_MODEL}")
    print(f"System instructions for LLM:")
    for key, value in settings.LLM_STRUCTURED_OUTPUT_SYSTEM_INSTRUCTIONS.items():
        print(f"    {key}: {value}")
