import logging
import os
import readline
import sys
from pathlib import Path
from typing import Callable

import black
import click

from everything.utils.magic import generate_function
from everything.utils.scanner import build_context_strings

_LOGGER = logging.getLogger(__name__)

EVERYTHING_CONTEXT_RADIUS = int(os.getenv("CONTEXT_RADIUS", "4"))
EVERYTHING_HISTORY = int(os.getenv("HISTORY", "10"))


def runtime_generate_function(
    name: str, context_radius: int = EVERYTHING_CONTEXT_RADIUS, history: int = EVERYTHING_HISTORY
) -> Callable:
    import __main__ as main

    if not hasattr(main, "__file__"):
        _LOGGER.info("Using REPL mode")
        readline.get_current_history_length()
        last_few_commands = [readline.get_history_item(i) for i in range(1, history)]
        context_string = "\n".join(last_few_commands)
    else:
        _LOGGER.info("Using SOURCE mode")
        source_path = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
        context_string = build_context_strings(source_path, name, context_radius)[name]

    return generate_function(
        name, context_string
    )  # pyright: ignore (impossible to type check)


def build_onefile_module(root_path: Path, module: str, **kwargs) -> str:
    functions = []
    for function_name, context_string in build_context_strings(
        root_path, module, **kwargs
    ).items():
        click.echo(f"Generating {function_name}...")
        functions.append(generate_function(function_name, context_string, True))
    source = "\n\n".join(functions)
    source = black.format_str(source, mode=black.FileMode()).strip()
    return source
