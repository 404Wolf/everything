import ast
from pathlib import Path

from typing_extensions import override


def find_function_calls_in_source(source_code: str, function_name: str) -> list[int]:
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

    return visitor.calls


def find_function_calls_in_dir(
    root: Path, function_name: str
) -> list[tuple[Path, int]]:
    """
    Find all the calls to a function in a directory.

    Args:
        root: The root directory to search in.
        function_name: The name of the function to search for.

    Returns:
        A list of tuples with the path to the file and the line number where the function is.
    """
    function_calls = []
    for path in root.rglob("*.py"):
        with open(path) as file:
            source_code = file.read()
        calls = find_function_calls_in_source(source_code, function_name)
        for call in calls:
            function_calls.append((path, call))
    return function_calls
