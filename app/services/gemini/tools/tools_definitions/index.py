from google.genai import types

from .calendar_def import calendar_functions
from .responses_def import response_function

function_definitions = {**calendar_functions, **response_function}

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
