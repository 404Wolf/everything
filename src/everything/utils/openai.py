from typing import Iterable, Callable
import re
import os
import logging

import openai
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

_LOGGER = logging.getLogger(__name__)

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class OpenAiMisbehaving(Exception):
    pass


def ask_ai(messages: Iterable[ChatCompletionMessageParam]) -> str:
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    if message := response.choices[0].message.content:
        return message
    else:
        raise OpenAiMisbehaving()


class FunctionGenerateFailure(Exception):
    pass


def generate_function(name: str, context: str, source: bool = False) -> Callable | str:
    """
    Generate a function based on a given context.

    Args:
        name: The name of the function to generate.
        context: The context to generate the function from.
        source: Whether to return the raw source code or a python function.

    Returns:
        A function that can be called with the same arguments as the generated function.
    """
    ai_messages = [
        {"role": "system", "content": "Provide a Python 3 valid function."},
        {
            "role": "system",
            "content": "Only provide the function. Do not say anything else.",
        },
        {
            "role": "user",
            "content": "HOW THE FUNCTION IS USED:# print hello world\nprint(hello_world())\n\ndef hello_world",
        },
        {
            "role": "assistant",
            "content": "def hello_world():\n    print('Hello, World!')",
        },
        {"role": "system", "content": ""},
        {
            "role": "user",
            "content": f"HOW THE FUNCTION IS USED:\n${context}\n\ndef {name}",
        },
    ]
    for _ in range(5):
        generated_function = ask_ai(ai_messages)
        _LOGGER.debug("Generated function: \n%s", generated_function)

        function_name = re.findall(
            r"def (\w[\w\d]+)\(", generated_function.split("\n")[0]
        )
        if function_name is None:
            raise FunctionGenerateFailure()
        else:
            try:
                function_name = function_name[0]
                _LOGGER.debug(f"Function generated had name {function_name}")
            except IndexError:
                continue

        if source:
            # Replace the function name in the result with the name we were asked for
            generated_function = re.sub(
                r"def (\w[\w\d]+)(", f"def {name}", generated_function
            )
            return generated_function

        def the_thing(*args, **kwargs):
            exec(generated_function)
            context = locals()
            exec(f"result = {function_name}(*args,**kwargs)", context)
            return context["result"]

        return the_thing
