from core import settings

if __name__ == "__main__":
    print("--- Loaded Settings ---")
    print(f"Project name: {settings.PROJECT_NAME}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"DEBUG - Chat history file: {settings.DEBUG_CHAT_HISTORY_FILE_PATH}")
    print(f"DEBUG - LLM context file: {settings.DEBUG_LLM_CONTEXT_FILE_PATH}")
    print(f"DEBUG - Courses file: {settings.DEBUG_COURSES_FILE_PATH}")
    print(f"Google API Key: {'Configurada' if settings.GOOGLE_API_KEY.get_secret_value() else 'NÃO CONFIGURADA'}")
    print(f"Basic LLM: {settings.GOOGLE_BASIC_MODEL}")
    print(f"Advanced LLM: {settings.GOOGLE_ADVANCED_MODEL}")
    print(f"Chat system instructions: {settings.CHAT_SYSTEM_INSTRUCTIONS}")
    print(f"Supported file types: {settings.SUPPORTED_FILE_TYPES}")
