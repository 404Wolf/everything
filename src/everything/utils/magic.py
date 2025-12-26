import logging
import os
import re
from typing import Callable

from anthropic import Anthropic
from anthropic.types import TextBlock

from .misc import (
    extract_from_codeblock_if_in_codeblock,
    str_function_to_real_function,
)

_LOGGER = logging.getLogger(__name__)

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
ANTHROPIC_MAX_TOKENS = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "4096"))
client = Anthropic()  # uses ANTHROPIC_API_KEY by default


class AnthropicMisbehaving(Exception):
    pass


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

    for _ in range(3):
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=ANTHROPIC_MAX_TOKENS,
            system="""
You generate valid Python 3 functions based on usage examples. Infer the function's structure, including inputs and outputs, from the provided context. The function should work immediately when dropped into the codebase.

Only provide the function code in a Python code block. Do not bother including type hints or docstrings, you want to maximize the chance that the code you plop into the program "just works."

Infer the function's behavior from:
    - Comments near the function
    - Type annotations showing how the function is used
    - Variable names, function names, and surrounding context
""",
            messages=[
                {
                    "role": "user",
                    "content": """# Example Usage:

```python
# print hello world
print(hello_world())
result = hello_world("Wolf")
```""",
                },
                {
                    "role": "assistant",
                    "content": """```python
def hello_world(name):
    return f'Hello, {name}!'
```""",
                },
                {
                    "role": "user",
                    "content": """# Example Usage:

```python
result = add(5, 3)
print(result)

def random_math():
    result = add(5, "333")
    works = result + 5 == 341
    print(works)
```""",
                },
                {
                    "role": "assistant",
                    "content": """```python
def add(a, b):
    return a + b
```""",
                },
                {
                    "role": "user",
                    "content": """# Example Usage:

```python
import requests
# get google homepage as text
html_content = get_google()
print(html_content[:100])
```""",
                },
                {
                    "role": "assistant",
                    "content": """```python
import requests

def get_google():
    response = requests.get('https://www.google.com')
    return response.text
```""",
                },
                {"role": "user", "content": f"# Example Usage:\n{context}"},
            ],
        )

        if response.content and isinstance(response.content[0], TextBlock):
            generated_function = response.content[0].text
        else:
            raise AnthropicMisbehaving()

        _LOGGER.debug("Generated function: \n%s", generated_function)

        generated_function = extract_from_codeblock_if_in_codeblock(generated_function)

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
                r"def (\w[\w\d]+)\(", f"def {name}(", generated_function
            )
            return generated_function

        return str_function_to_real_function(generated_function)

    raise FunctionGenerateFailure("Failed to generate function after 3 attempts")
