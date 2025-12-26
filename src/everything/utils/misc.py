import ast
import re
from typing import Callable


def extract_from_codeblock_if_in_codeblock(codeblock: str) -> str:
    """Extract code from a codeblock if it's in a codeblock"""
    match = re.match(r"```[^\n]*\n(.*?)```", codeblock, re.DOTALL)
    if match:
        return match.group(1).strip()
    return codeblock


def extract_inner_content_from_function(codeblock: str) -> str:
    """Extract the inner content of a function from a codeblock"""
    tree = ast.parse(codeblock)
    func = tree.body[0]
    if isinstance(func, ast.FunctionDef):
        return "\n".join(ast.unparse(stmt) for stmt in func.body)
    raise ValueError("Expected a function definition")


def str_function_to_real_function(code: str, scope: dict | None = None) -> Callable:
    """Convert a string representation of a function to a real function"""
    scope = scope or locals()
    exec(code, scope)
    return eval(code.split("def ")[1].split("(")[0], scope)
