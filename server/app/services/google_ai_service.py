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
                           instruction: str,
                           message: str,
                           llm_context: list[Content] | None = None
                           ) -> tuple[str, list[Content]]:
        user_content: Content = Content(role="user", parts=[Part(text=message)])
        contents: list[Content] = list(llm_context) if llm_context else []
        contents.append(user_content)
        response = (await self.client.aio.models.generate_content(
            model=settings.GOOGLE_ADVANCED_MODEL,
            contents=contents,
            config=GenerateContentConfig(
                system_instruction=instruction))).text
        model_content: Content = Content(role="model", parts=[Part(text=response)])
        return response, [user_content, model_content]

    async def generate_structured_output(self,
                                         instruction: str,
                                         schema: type[BaseModel],
                                         files: list[tuple[bytes, str]],
                                         message: str | None = None
                                         ) -> BaseModel:
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
        return schema.model_validate_json(response)


async def create_content_from_files(role: str, files: list[tuple[bytes, str]]) -> Content:
    parts = [Part(inline_data=Blob(data=data, mime_type=mime))
             for data, mime in files]
    return Content(role=role, parts=parts)


if not settings.GOOGLE_API_KEY or not settings.GOOGLE_API_KEY.get_secret_value():
    class DummyGoogleAIService:
        async def send_message(self, *args, **kwargs):
            return "Resposta fake do mock", []
        async def generate_structured_output(self, *args, **kwargs):
            return '''
            {
                "uuid": "mock-uuid-123",
                "title": "Matemática Mock",
                "semester": "2025.1",
                "lectures": [
                    {
                        "title": "Aula 1",
                        "start_datetime": "2025-03-01T08:00:00",
                        "end_datetime": "2025-03-01T10:00:00",
                        "summary": "Introdução ao mock"
                    }
                ],
                "evaluations": [
                    {
                        "type": "exam",
                        "title": "Prova 1",
                        "start_datetime": "2025-04-01T08:00:00",
                        "end_datetime": "2025-04-01T10:00:00"
                    }
                ]
            }
            '''
    google_ai_service = DummyGoogleAIService()
else:
    google_ai_service = GoogleAIService(api_key=settings.GOOGLE_API_KEY.get_secret_value())
