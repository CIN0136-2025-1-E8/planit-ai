import os
import pickle

from google.genai.types import Content

from core import settings
from schemas import ChatMessage


def get_chat_crud():
    return chat_crud


class CRUDChat:
    def __init__(self):
        self.llm_context: list[Content] = []
        self.read_llm_context_from_file()
        self.chat_history: list[ChatMessage] = []
        self.read_chat_history_from_file()

    def read_llm_context_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_LLM_CONTEXT_FILE_PATH):
            with open(settings.DEBUG_LLM_CONTEXT_FILE_PATH, 'rb') as file:
                self.llm_context = pickle.load(file)
        return

    def write_llm_context_to_file(self) -> None:
        with open(settings.DEBUG_LLM_CONTEXT_FILE_PATH, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.llm_context, f)
        return

    def get_llm_context(self) -> list[Content] | None:
        return self.llm_context

    def append_llm_context(self, new_content: list[Content]) -> None:
        self.llm_context.extend(new_content)
        self.write_llm_context_to_file()
        return

    def read_chat_history_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_CHAT_HISTORY_FILE_PATH):
            with open(settings.DEBUG_CHAT_HISTORY_FILE_PATH, 'rb') as file:
                self.chat_history = pickle.load(file)
        return

    def write_chat_history_to_file(self) -> None:
        with open(settings.DEBUG_CHAT_HISTORY_FILE_PATH, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.chat_history, f)
        return

    def get_chat_history(self) -> list[ChatMessage] | None:
        return self.chat_history

    def append_chat_history(self, chat_message: ChatMessage) -> None:
        self.chat_history.append(chat_message)
        self.write_chat_history_to_file()


chat_crud = CRUDChat()
