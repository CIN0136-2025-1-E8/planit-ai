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
    DEBUG_COURSES_FILE_PATH: Path = BASE_DIR / ".venv/courses.pkl"

    GOOGLE_API_KEY: Optional[SecretStr] = None
    GOOGLE_BASIC_MODEL: str = "gemma-3-27b-it"
    GOOGLE_ADVANCED_MODEL: str = "gemini-2.0-flash"

    SYSTEM_MESSAGE_MARKER_START: str = "[PlanIt AI - System Message - START]: "
    SYSTEM_MESSAGE_MARKER_END: str = " :[PlanIt AI - System Message - END]\n"

    CHAT_SYSTEM_INSTRUCTIONS: str = (
        "The system can send information to you as messages that begin with '[PlanIt AI - System Message - START]:' "
        "and conclude with ':[PlanIt AI - System Message - END]'. These messages may or may not contain JSON "
        "formatted data. System messages are not visible in the chat UI but serve as crucial context for generating "
        "accurate responses. When the system provides details about a newly enrolled course or an update to an "
        "existing one, inform the user naturally that you've noted the addition and offer assistance related to this "
        "new information. Always respond in the language inferred from the user's message history, unless explicitly "
        "requested otherwise. Format all date, time, and currency data according to the region inferred from the "
        "user's message history. If a user asks you to perform an action, such as creating, updating or deleting an "
        "object from their study plan, that requires a tool that is not available to you, politely explain that "
        "you're not yet able to perform such actions. Only generate responses in code or JSON if requested. If the "
        "user requests information or an action that requires date or time information, use your tools to get the "
        "current UTC time."
    )

    SUPPORTED_FILE_TYPES: list[str] = ["application/pdf",
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
                                       "image/heif"]

    DATABASE_URL: Optional[str] = None

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
