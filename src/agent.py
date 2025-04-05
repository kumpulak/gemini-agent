"""Wrapper for Google's Generative AI v1alpha Live API."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from google import genai
from google.genai import live, types

from utils import create_response, parse_function

if TYPE_CHECKING:
    from collections.abc import Callable

load_dotenv()


class Agent:
    """Wrapper for Gemini with tools."""

    def __init__(
        self,
        model: str,
        system_instruction: str | None = None,
    ) -> None:
        """Initialize agent with a model."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key must be provided in GEMINI_API_KEY environment variable")

        self.client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})
        self.model = model
        self.system_instruction = system_instruction
        self.tool_functions: dict[str, Callable] = {}
        self.tool_declarations: list[dict] = []

    def add_tool(self, tool: Callable) -> None:
        """Register a callable function as a tool."""
        func_name = tool.__name__
        declaration = parse_function(tool)

        self.tool_declarations.append(declaration)
        self.tool_functions[func_name] = tool

    async def _execute_tool_call(self, session: live.AsyncLiveClientSession, tool_call: types.ToolCall) -> None:
        """Execute function calls and send results back to the model."""
        responses = []

        for function_call in tool_call.function_calls:
            response = create_response(function_call, self.tool_functions)
            responses.append(response)

        if responses:
            await session.send(input=types.LiveClientToolResponse(function_responses=responses))

    async def run(
        self,
        task: str,
        *,
        enable_code_execution: bool = True,
        enable_google_search: bool = False,
    ) -> str:
        """Execute a task with the model and return its response."""
        tools = []
        if self.tool_declarations:
            tools.append(types.Tool(function_declarations=self.tool_declarations))
        if enable_code_execution:
            tools.append(types.Tool(code_execution=types.ToolCodeExecution()))
        if enable_google_search:
            tools.append(types.Tool(google_search=types.GoogleSearch()))

        config = {
            "tools": tools,
            "response_modalities": ["TEXT"],
        }

        if self.system_instruction:
            config["system_instruction"] = self.system_instruction

        try:
            async with self.client.aio.live.connect(model=self.model, config=config) as session:
                await session.send(input=task, end_of_turn=True)

                final_response = []
                async for response in session.receive():
                    if text := response.text:
                        final_response.append(text)
                    elif tool_call := response.tool_call:
                        for fc in tool_call.function_calls:
                            args_str = ", ".join(f"{k}='{v}'" for k, v in fc.args.items())
                            tool_info = f"\n🔧 **Tool**: `{fc.name}({args_str})`\n\n"
                            final_response.append(tool_info)

                        await self._execute_tool_call(session, tool_call)

                return "".join(final_response).strip()

        except Exception as e:
            print(f"Error during Live API session: {e}")
            return f"Error: {e}"
