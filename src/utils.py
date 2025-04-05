"""Utilities for Gemini agent functionality."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from google.genai import types

if TYPE_CHECKING:
    from collections.abc import Callable

# Type mapping from Python types to OpenAPI schema types
TYPE_MAP: dict[type, str] = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def get_python_type(annotation: type | Any) -> str:
    """Convert Python type annotations to OpenAPI schema type strings.

    Args:
        annotation: The Python type annotation to convert.

    Returns:
        The corresponding OpenAPI type string.
    """
    if isinstance(annotation, type):
        mapped_type = TYPE_MAP.get(annotation)
        if mapped_type:
            return mapped_type
        for py_type, openapi_type in TYPE_MAP.items():
            try:
                if issubclass(annotation, py_type):
                    return openapi_type
            except TypeError:
                continue
    return "string"


def parse_function(tool: Callable) -> dict:
    """Parse a callable function into a Gemini tool declaration.

    Args:
        tool: A callable function to convert to a tool declaration.

    Returns:
        A dictionary containing the function declaration in Gemini format.

    Raises:
        TypeError: If the provided tool is not a callable.
    """
    func_name = tool.__name__

    sig = inspect.signature(tool)
    description = inspect.getdoc(tool) or f"Executes the {func_name} function."

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        param_type = get_python_type(param.annotation)
        properties[name] = {
            "type": param_type,
            "description": f"Parameter {name}",
        }

        if param.default is inspect.Parameter.empty:
            required.append(name)

    declaration = {
        "name": func_name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }

    return declaration


def create_response(function_call: types.FunctionCall, tool_functions: dict[str, Callable]) -> types.FunctionResponse:
    """Create a function response for a tool call."""
    if function_call.name not in tool_functions:
        return types.FunctionResponse(
            name=function_call.name,
            id=function_call.id,
            response={"error": f"Function {function_call.name} not implemented by agent"},
        )

    try:
        result = tool_functions[function_call.name](**function_call.args)
        return types.FunctionResponse(name=function_call.name, id=function_call.id, response={"result": result})
    except Exception as e:
        return types.FunctionResponse(name=function_call.name, id=function_call.id, response={"error": str(e)})
