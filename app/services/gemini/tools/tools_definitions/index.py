from google.genai import types

from .calendar_def import calendar_functions

function_definitions = {
    **calendar_functions,
}

tools = [
    types.Tool(
        function_declarations=[
            {
                "name": name,
                "description": data["description"],
                "parameters": data["parameters"],
            }
            for name, data in function_definitions.items()
        ]
    )
]
