import asyncio
from .tools_definitions.index import function_definitions
from google.genai import types
from fastapi import Request


async def execute_function_call(function_call: types.FunctionCall, request: Request):
    fn_name = function_call.name
    parameters = function_call.args or {}
    fetcher = function_definitions.get(fn_name, {}).get("fetcher")
    fn_type = function_definitions.get(fn_name, {}).get("type") or "function"
    if not fetcher:
        return types.Part.from_function_response(
            name=fn_name,
            response={"error": f"No fetcher defined for function '{fn_name}'"},
        )

    try:
        if asyncio.iscoroutinefunction(fetcher):
            data = await fetcher(**parameters, request=request)
        else:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, lambda: fetcher(**parameters, request=request)
            )

        return types.Part.from_function_response(
            name=fn_name,
            response={"result": data},
        )

    except Exception as e:
        return types.Part.from_function_response(
            name=fn_name,
            response={"error": str(e)},
        )


async def process_function_calls(
    function_calls: list[types.FunctionCall], request: Request
):
    tasks = [execute_function_call(fn, request) for fn in function_calls]
    return await asyncio.gather(*tasks)
