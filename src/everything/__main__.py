from pathlib import Path

import click

from everything.generator import build_onefile_module
from everything.utils.scanner import get_module_function_contexts


@click.group()
def cli():
    pass


@click.command()
@click.argument("source", default=".")
@click.argument("destination", default="everything")
@click.option(
    "--onefile",
    default=False,
    is_flag=True,
    help="Generate the magic library as a single python file",
)
@click.option(
    "--usage-name",
    default="everything",
    help="The name used when using the module in your source code",
)
@click.option(
    "--context-radius",
    default=4,
    help="The radius around all function usages to provide as context to the LLM",
)
def build(
    source: str, destination: str, onefile: bool, usage_name: str, context_radius
):
    """Build a magic library based on how you use it.

    `src` is The source directory to scan for building the module.
    """
    click.echo(f"Building module used as {usage_name} from {source} in {destination}.")
    if onefile:
        output = build_onefile_module(Path(source), usage_name, radius=context_radius)
        with open(destination, "w") as file:
            file.write(output)
        click.echo("Wrote output file")
    else:
        output = get_module_function_contexts(Path(source), usage_name)
    print(output)


cli.add_command(build)
