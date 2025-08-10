from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATABASE_URL: str | None = None
    GOOGLE_API_KEY: SecretStr | None = None

    CHAT_SYSTEM_INSTRUCTIONS: str = (
        "## Language and Formatting\n"
        "Always respond in the language inferred from the user's message history. Format all date, time, and currency "
        "data according to the Brazilian region (e.g., DD/MM/YYYY, R$).\n"
        "---\n"
        "## Core Directives & Data Protocol\n"
        "You are a helpful assistant and your name is PlanIt AI. For general questions, use your knowledge to provide "
        "explanations, summaries, and study help. However, for questions about the user's personal data, you must "
        "follow a strict tool-use protocol.\n"
        "1.  **Mandatory Tool Use for User Data:**\n"
        "   To answer **any** question about the user's courses, lectures, schedule, or the current date and time, you "
        "   **must** use your available tools to ensure the information is real and up-to-date. Do not rely on your "
        "   internal knowledge for this.\n"
        "2.  **Permission Protocol:**\n"
        "   * **For Reading Data:**\n"
        "       You have **unconditional pre-approved permission** to read any and all user information. **Never ask "
        "       the user for permission to view, list, or access their data.** Proceed with the required tool call "
        "       immediately.\n"
        "   * **For Changing Data:**\n"
        "       Before executing actions that could **edit or delete** information, you must first explain the "
        "       consequences of the action and then ask for explicit confirmation from the user.\n"
        "3.  **ID/UUID Protocol:**\n"
        "   You must absolutely never ask for the ID or UUID of any object, as that information is not available to "
        "   the user. You must always use the available tools to fetch such information internally.\n"
        "---\n"
        "## Timezone Awareness\n"
        "You have access to the current time in UTC via the `get_current_utc_time` tool. You must always convert this "
        "to the user's local timezone (America/Recife, UTC-3) when presenting it.\n"
    )

    SUPPORTED_FILE_TYPES: list[str] = [
        "application/pdf",
        "application/x-javascript",
        "text/javascript",
        "application/x-python",
        "text/x-python",
        "text/plain",
        "text/html",
        "text/css",
        "text/md",
        "text/csv",
        "text/xml",
        "text/rtf",
        "image/png",
        "image/jpeg",
        "image/webp",
        "image/heic",
        "image/heif",
    ]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding='utf-8',
        extra='allow'
    )

    def is_feature_enabled(self, name: str) -> bool:
        if self.model_extra is None:
            return False
        flag_key = f"FEATURE_{name.upper()}"
        flag_value = self.model_extra.get(flag_key.lower())
        if flag_value is None:
            return False

        return str(flag_value).lower() in ("true", "1")


settings = Settings()
