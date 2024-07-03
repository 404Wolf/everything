import logging
import os
import re
import readline
import sys
from pathlib import Path

from everything.utils.ai import ask_ai
from everything.utils.usages import find_function_calls_in_dir

_LOGGER = logging.getLogger()


def make_the_thing(name, context=4, history=10):
    import __main__ as main

    example_template = "HOW THE FUCTION IS USED:\n"
    if not hasattr(main, "__file__"):
        readline.get_current_history_length()
        last_few_commands = [readline.get_history_item(i) for i in range(1, history)]
        context_for_function_bulder = example_template
        context_for_function_bulder += "\n".join(last_few_commands)
    else:
        context_for_function_bulder = example_template
        source_path = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
        function_calls = find_function_calls_in_dir(source_path, name)
        for function_file, function_line in function_calls:
            _LOGGER.debug("Function call found in %s:%s", function_file, function_line)
            function_file_code = function_file.read_text()
            function_file_lines = function_file_code.split("\n")
            if "import" in function_file_lines[function_line]:
                continue
            start_line = max(0, function_line - context)
            end_line = min(len(function_file_lines), function_line + context)
            function_snippet = "\n".join(function_file_lines[start_line:end_line])
            context_for_function_bulder += (
                f"{function_file.name}:{function_line}\n{function_snippet}\n"
            )
            context_for_function_bulder += "=" * 20 + "\n"

    _LOGGER.debug("Context for function builder:\n%s", context_for_function_bulder)

    generated_function = ask_ai(
        [
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
                "content": f"HOW THE FUNCTION IS USED:\n${context_for_function_bulder}\n\ndef {name}",
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
