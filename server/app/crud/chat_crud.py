import os
import pickle

from google.genai.types import Content

from app.core import settings
from app.schemas import ChatMessage


def get_chat_crud():
    return chat_crud


class CRUDChat:
    def __init__(self,
                 llm_context_file_path: str = settings.DEBUG_LLM_CONTEXT_FILE_PATH,
                 chat_history_file_path: str = settings.DEBUG_CHAT_HISTORY_FILE_PATH):
        self.llm_context: list[Content] = []
        self.read_llm_context_from_file(llm_context_file_path)
        self.chat_history: list[ChatMessage] = []
        self.read_chat_history_from_file(chat_history_file_path)

    def read_llm_context_from_file(self, file_path: str = settings.DEBUG_LLM_CONTEXT_FILE_PATH) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.llm_context = pickle.load(file)
        return

    def write_llm_context_to_file(self, file_path: str = settings.DEBUG_LLM_CONTEXT_FILE_PATH) -> None:
        with open(file_path, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.llm_context, f)
        return

    def get_llm_context(self) -> list[Content] | None:
        return self.llm_context

    def append_llm_context(self, new_content: list[Content]) -> None:
        self.llm_context.extend(new_content)
        return

    def read_chat_history_from_file(self, file_path: str = settings.DEBUG_CHAT_HISTORY_FILE_PATH) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.chat_history = pickle.load(file)
        return

    def write_chat_history_to_file(self, file_path: str = settings.DEBUG_CHAT_HISTORY_FILE_PATH) -> None:
        with open(file_path, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.chat_history, f)
        return

    def get_chat_history(self) -> list[ChatMessage] | None:
        return self.chat_history

    def append_chat_history(self, chat_message: ChatMessage) -> None:
        self.chat_history.append(chat_message)


chat_crud = CRUDChat()
