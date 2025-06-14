import os
import pickle

from core import settings
from schemas import BasicChatHistory


class CRUDBasicChat:
    history = {}

    def read_history_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_HISTORY_FILE_PATH):
            with open(settings.DEBUG_HISTORY_FILE_PATH, 'rb') as file:
                self.history = pickle.load(file)
        return

    def write_history_to_file(self) -> None:
        with open(settings.DEBUG_HISTORY_FILE_PATH, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.history, f)
        return

    def get_chat_history_by_session_id(self, session_id: str) -> BasicChatHistory | None:
        if session_id in self.history:
            return BasicChatHistory(session_id=session_id, history=self.history[session_id])
        return None

    def set_chat_history_by_session_id(self, chat_history: BasicChatHistory) -> None:
        self.history[chat_history.session_id] = chat_history.history
        self.write_history_to_file()
        return


basic_chat_crud = CRUDBasicChat()
