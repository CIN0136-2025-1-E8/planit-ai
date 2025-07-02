import os
import pickle

from google.genai.types import Content

from core import settings


def get_chat_crud():
    return chat_crud


class CRUDChat:
    def __init__(self):
        self.llm_context: list[Content] = []
        self.read_llm_context_from_file()

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

    def set_llm_context(self, llm_context: list[Content]) -> None:
        self.llm_context = llm_context
        self.write_llm_context_to_file()
        return


chat_crud = CRUDChat()
