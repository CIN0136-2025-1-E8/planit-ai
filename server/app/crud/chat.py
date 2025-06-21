import json
import os

from core import settings
from schemas import ChatMessageParts, ChatHistory, ChatsList


class CRUDChat:
    history: dict[str, list[ChatMessageParts]] = {}

    def read_history_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_CHAT_HISTORY_FILE_PATH):
            with open(settings.DEBUG_CHAT_HISTORY_FILE_PATH, 'r', encoding='utf-8') as f:
                history_from_json = json.load(f)
            self.history = {
                session_id: [ChatMessageParts.model_validate(message) for message in chat]
                for session_id, chat in history_from_json.items()
            }
        return

    def write_history_to_file(self) -> None:
        history_serializable = {
            session_id: [message.model_dump(mode='json') for message in chat]
            for session_id, chat in self.history.items()
        }
        with open(settings.DEBUG_CHAT_HISTORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(history_serializable, f, indent=4, ensure_ascii=False)
        return

    def get_user_chats_list(self) -> ChatsList | None:
        if self.history:
            return ChatsList(session_ids=list(self.history.keys()))
        return None

    def get_chat_history_by_session_id(self, session_id: str | None) -> ChatHistory | None:
        if session_id in self.history:
            return ChatHistory(session_id=session_id, history=self.history[session_id])
        return None

    def set_chat_history_by_session_id(self, chat_history: ChatHistory) -> None:
        self.history[chat_history.session_id] = chat_history.history
        self.write_history_to_file()
        return

    def append_to_history_by_session_id(self, session_id: str, part: ChatMessageParts) -> None:
        if session_id not in self.history:
            self.history[session_id] = []
        self.history[session_id].append(part)
        self.write_history_to_file()
        return


chat_crud = CRUDChat()
