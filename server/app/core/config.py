from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, SecretStr
from typing import Optional


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    PROJECT_NAME: str = "PlanIt AI"
    DEBUG: bool = False
    DEBUG_HISTORY_FILE_PATH: Path = BASE_DIR / ".venv/history.pkl"

    GOOGLE_API_KEY: Optional[SecretStr] = None
    GOOGLE_MODEL: str = "gemma-3-27b-it"

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
    print(f"Modelo: {settings.GOOGLE_MODEL}")

    print("\nLembre-se de criar um arquivo '.env' na pasta 'server/' com os valores reais das suas chaves e segredos!")