from google import genai
from google.genai.types import Content, Part

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


google_ai_service = GoogleAIService(api_key=settings.GOOGLE_API_KEY.get_secret_value())
