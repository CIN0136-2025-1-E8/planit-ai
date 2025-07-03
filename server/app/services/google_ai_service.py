from google import genai
from google.genai.types import Content, Part, Blob, GenerateContentConfig
from pydantic import BaseModel

from core import settings


def get_google_ai_service():
    return google_ai_service


class GoogleAIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google API key not configured.")
        self.client = genai.Client(api_key=api_key)

    async def send_message(self,
                           message: str,
                           llm_context: list[Content] | None = None
                           ) -> tuple[str, list[Content]]:
        chat = self.client.aio.chats.create(model=settings.GOOGLE_BASIC_MODEL, history=llm_context)
        response = (await chat.send_message(message)).text
        return (response, [Content(role="user", parts=[Part(text=message)]),
                           Content(role="model", parts=[Part(text=response)])])

    async def generate_structured_output(self,
                                         instruction: str,
                                         schema: type[BaseModel],
                                         files: list[tuple[bytes, str]],
                                         message: str | None = None
                                         ) -> str:
        content: Content = await create_content_from_files(role="user", files=files)
        if message:
            content.parts.append(Part(text=message))
        response: str = (await self.client.aio.models.generate_content(
            model=settings.GOOGLE_ADVANCED_MODEL,
            contents=content,
            config=GenerateContentConfig(
                system_instruction=instruction,
                response_mime_type="application/json",
                response_schema=schema))).text
        return response


async def create_content_from_files(role: str, files: list[tuple[bytes, str]]) -> Content:
    parts = [Part(inline_data=Blob(data=data, mime_type=mime))
             for data, mime in files]
    return Content(role=role, parts=parts)


google_ai_service = GoogleAIService(api_key=settings.GOOGLE_API_KEY.get_secret_value())
