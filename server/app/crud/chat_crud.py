import os
import pickle

from google.genai.types import Content

from core import settings


def get_chat_crud():
    return chat_crud


class CRUDChat:
    def __init__(self):
        self.history: list[Content] = []
        self.read_history_from_file()

    def read_history_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_CHAT_HISTORY_FILE_PATH):
            with open(settings.DEBUG_CHAT_HISTORY_FILE_PATH, 'rb') as file:
                self.history = pickle.load(file)
        return

    def write_history_to_file(self) -> None:
        with open(settings.DEBUG_CHAT_HISTORY_FILE_PATH, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.history, f)
        return

    def get_chat_history(self) -> list[Content] | None:
        return self.history

    def set_chat_history(self, chat_history: list[Content]) -> None:
        self.history = chat_history
        self.write_history_to_file()
        return


chat_crud = CRUDChat()
