import logging
import re

from dopy.utils.ai import ask_ai

_LOGGER = logging.getLogger()


def make_the_thing(name):
    generated_function = ask_ai(
        [
            {"role": "system", "content": "Provide a Python 3 valid function."},
            {
                "role": "system",
                "content": "Only provide the function. Do not say anything else.",
            },
            {"role": "user", "content": "def hello_world"},
            {
                "role": "assistant",
                "content": "def hello_world():\n    return 'Hello, World!'",
            },
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": f"def {name}",
            },
        ]
    )
    _LOGGER.debug("Generated function: \n%s", generated_function)

    def error():
        raise SyntaxError("Function not generated correctly.")

    function_name = re.findall(r"def (\w[\w\d]+)\(", generated_function.split("\n")[0])
    function_name = function_name[0] if function_name is not None else "error"
    _LOGGER.debug(f"Function generated had name {function_name}")

    def the_thing(*args, **kwargs):
        exec(generated_function)
        context = locals()
        exec(f"result = {function_name}(*args,**kwargs)", context)
        return context["result"]

    return the_thing
