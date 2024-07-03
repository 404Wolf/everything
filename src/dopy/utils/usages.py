import ast
import inspect
import os
from dataclasses import dataclass
from pathlib import Path

from typing_extensions import override


@dataclass(frozen=True)
class FunctionCall:
    line_number: int
    function_name: str

    def __str__(self) -> str:
        return f"{self.function_name} called at line {self.line_number}"

    def content(self, source_code: str, context: int = 0) -> str:
        """
        Get the source code of the function call.

        Args:
            source_code: The source code of the script.
            context: The number of lines to include before and after the function call.
        """
        lines = source_code.splitlines()
        start = max(0, self.line_number - 1 - context)
        end = min(len(lines), self.line_number + context)
        return "\n".join(lines[start:end])


def find_function_calls(source_code: str, function_name: str) -> list[FunctionCall]:
    """
    Find all the calls to a function in the source code.

    Args:
        source_code: The source code of the script.
        function_name: The name of the function to search for.

    Returns:
        A list of line numbers where the function is called.
    """

    class FunctionCallVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.calls: list[int] = []

        @override
        def visit_Call(self, node: ast.Call) -> None:
            if isinstance(node.func, ast.Name) and node.func.id == function_name:
                self.calls.append(node.lineno)
            self.generic_visit(node)

    tree = ast.parse(source_code)
    visitor = FunctionCallVisitor()
    visitor.visit(tree)

    calls = visitor.calls
    function_calls = []
    for call in calls:
        function_calls.append(
            FunctionCall(line_number=call, function_name=function_name)
        )
    return function_calls


def get_invoking_script_path(stack_index: int = 1) -> Path:
    """
    Get the absolute path of the script that invokes this function.

    Returns:
        The path to the file being interpreted.
    """
    # Get the frame object of the caller
    frame = inspect.stack()[stack_index]
    caller_filepath = frame.filename

    script_path = os.path.abspath(caller_filepath)
    return Path(script_path)


def get_invoking_script_contents() -> str:
    """Get the contents of the script that invokes this function."""
    return get_invoking_script_path(2).read_text() or ""
