import mimetypes
from typing import AsyncGenerator

from google import genai
from google.genai.types import Blob, Content, Part

from core import settings
from schemas import ChatPartTypes, ChatMessageParts, ChatHistory
from utils.file_handling import get_buffered_reader_from_filename


class GoogleAIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google API key not configured.")
        self.client = genai.Client(api_key=api_key)

    async def send_message(self,
                           model: str,
                           message: ChatMessageParts,
                           chat_history: ChatHistory | None = None
                           ) -> str:
        contents: list[Content] = chat_history_to_content_list(chat_history) if chat_history else []
        contents.append(Content(role="user", parts=chat_message_parts_to_part_list(message)))
        response = await self.client.aio.models.generate_content(model=model, contents=contents)
        return response.text

    async def send_message_stream_response(self,
                                           model: str,
                                           message: ChatMessageParts,
                                           chat_history: ChatHistory | None = None
                                           ) -> AsyncGenerator[str, None]:
        contents: list[Content] = chat_history_to_content_list(chat_history) if chat_history else []
        contents.append(Content(role="user", parts=chat_message_parts_to_part_list(message)))

        async def streaming_chat_message():
            async for chunk in await self.client.aio.models.generate_content_stream(model=model, contents=contents):
                if chunk.text:
                    yield chunk.text

        return streaming_chat_message()


def chat_message_parts_to_part_list(chat_message_parts: ChatMessageParts) -> list[Part]:
    parts: list[Part] = []
    for part in chat_message_parts.parts:
        if part.type == ChatPartTypes.TEXT:
            parts.append(Part(text=part.content))
        elif part.type == ChatPartTypes.FILE:
            parts.append(Part(inline_data=Blob(
                mime_type=mimetypes.guess_type(part.content)[0],
                data=get_buffered_reader_from_filename(part.content).read()), ))
    return parts


def chat_history_to_content_list(chat_history: ChatHistory | None) -> list[Content] | None:
    if chat_history is None:
        return None
    contents: list[Content] = []
    for message in chat_history.history:
        parts: list[Part] = chat_message_parts_to_part_list(message)
        contents.append(Content(
            role=message.role.value,
            parts=parts))
    return contents


google_ai_service = GoogleAIService(api_key=settings.GOOGLE_API_KEY.get_secret_value())
