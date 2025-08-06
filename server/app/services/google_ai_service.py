import asyncio
import inspect
import json

from google import genai
from google.genai.types import Content, Part, Blob, GenerateContentConfig, FunctionDeclaration, Tool, FunctionResponse, \
    ToolConfig, FunctionCallingConfig, FunctionCallingConfigMode
from pydantic import BaseModel

from app.core import settings
from app.llm_tools import tools

_MAX_CONTEXT_SIZE_BYTES = 20 * 1024 * 1024


def get_google_ai_service():
    return google_ai_service


class GoogleAIService:
    def __init__(self, api_key: str, client=None):
        if client:
            self.client = client
        else:
            if not api_key:
                raise ValueError("Google API key not configured.")
            self.client = genai.Client(api_key=api_key)

    def _get_contents_size(self, contents: list[Content]) -> int:
        """Calculates the approximate size of the content list in bytes."""
        dict_representation = [
            content.model_dump_json(exclude_none=True) for content in contents
        ]
        return len(json.dumps(dict_representation).encode('utf-8'))

    async def _trim_context_to_size(self, contents: list[Content]) -> list[Content]:
        """
        Trims the contents list from the beginning until it's under the size limit.
        It removes the oldest messages (user/model pairs) first.
        """
        current_size = self._get_contents_size(contents)
        while current_size > _MAX_CONTEXT_SIZE_BYTES:
            if len(contents) < 2:
                raise ValueError(
                    f"A single message part exceeds the {_MAX_CONTEXT_SIZE_BYTES / (1024 * 1024)}MB limit. "
                    "Cannot trim further."
                )

            del contents[0:2]
            current_size = self._get_contents_size(contents)
        return contents

    async def send_message(self,
                           instruction: str,
                           message: str,
                           files: list[tuple[bytes, str]] | None = None,
                           llm_context: list[Content] | None = None
                           ) -> tuple[str, list[Content]]:
        tool_map = {func.__name__: func for func in tools}
        function_declarations = [FunctionDeclaration.from_callable_with_api_option(callable=f) for f in tools]
        sdk_tools = [Tool(function_declarations=function_declarations)]

        all_parts = []
        if files:
            file_parts = await create_parts_from_files(files)
            all_parts.extend(file_parts)
        all_parts.append(Part(text=message))

        user_content = Content(role="user", parts=all_parts)
        contents = list(llm_context or [])
        contents.append(user_content)

        while True:
            contents = await self._trim_context_to_size(contents)
            response = await self.client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=GenerateContentConfig(
                    system_instruction=instruction,
                    tools=sdk_tools,
                    tool_config=ToolConfig(
                        function_calling_config=FunctionCallingConfig(mode=FunctionCallingConfigMode.AUTO)
                    )
                )
            )

            response_part = response.candidates[0].content.parts[0]
            if not response_part.function_call:
                final_text = response.text
                break

            contents.append(response.candidates[0].content)
            function_calls = [part.function_call for part in response.candidates[0].content.parts]

            tasks_to_run = []
            for call in function_calls:
                if call.name in tool_map:
                    func = tool_map[call.name]
                    args = dict(call.args)
                    if inspect.iscoroutinefunction(func):
                        tasks_to_run.append(func(**args))
                    else:
                        tasks_to_run.append(asyncio.to_thread(func, **args))

            tool_results = await asyncio.gather(*tasks_to_run)

            tool_response_parts = [
                Part(function_response=FunctionResponse(name=call.name, response=result))
                for call, result in zip(function_calls, tool_results)
            ]
            contents.append(Content(role="user", parts=tool_response_parts))

        model_content: Content = Content(role="model", parts=[Part(text=final_text)])
        return final_text, [user_content, model_content]

    async def generate_structured_output(self,
                                         schema: type[BaseModel],
                                         files: list[tuple[bytes, str]],
                                         instruction: str | None = None,
                                         message: str | None = None
                                         ) -> BaseModel:
        content: Content = await create_content_from_files(role="user", files=files)
        if message:
            content.parts.append(Part(text=message))
        response: str = (await self.client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=content,
            config=GenerateContentConfig(
                system_instruction=instruction,
                response_mime_type="application/json",
                response_schema=schema))).text
        try:
            start_index = response.index('{')
            end_index = response.rindex('}')
            response = response[start_index:end_index + 1]
        except ValueError:
            raise ValueError("Invalid JSON format: Couldn't find starting or ending braces.")
        return schema.model_validate_json(response)


async def create_parts_from_files(files: list[tuple[bytes, str]]) -> list[Part]:
    return [Part(inline_data=Blob(data=data, mime_type=mime)) for data, mime in files]


async def create_content_from_files(role: str, files: list[tuple[bytes, str]]) -> Content:
    parts = [Part(inline_data=Blob(data=data, mime_type=mime))
             for data, mime in files]
    return Content(role=role, parts=parts)


google_ai_service = GoogleAIService(api_key=settings.GOOGLE_API_KEY.get_secret_value())
