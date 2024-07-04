import ast
from typing import Generator
from dataclasses import dataclass
from pathlib import Path
from functools import wraps

__all__ = ["walk_directory"]


def keep_visiting(method):
    @wraps(method)
    def wrapper(self, node):
        result = method(self, node)
        self.generic_visit(node)
        return result

    return wrapper


class TraversalFile:
    def __init__(self, path: Path):
        self.path = path
        self.contents = path.read_text()

    def get_line(self, line: int):
        return self.contents.split("\n")[line]

    def get_context(self, line: int, radius: int = 4):
        lines = self.contents.split("\n")
        start_line = max(0, line - radius)
        end_line = min(len(lines), line + radius)
        return "\n".join(lines[start_line:end_line])

    def get_ast(self):
        return ast.parse(self.contents)


@dataclass(frozen=True)
class ReferencedFunction:
    name: str
    node: ast.ImportFrom | ast.Call | ast.Attribute

    @property
    def line_number(self):
        return self.node.lineno


class ModuleFunctionReferenceFinder(ast.NodeVisitor):
    def __init__(self, module: str, traversal_file: TraversalFile) -> None:
        self.module: str = module
        self.traversal_file: TraversalFile = traversal_file
        self.imported_functions: set[ReferencedFunction]  = set()
        self.function_references: set[ReferencedFunction] = set()
        self._possible_references = set()

    def find_references(self) -> Generator[ReferencedFunction, None, None]:
        # Visit the AST to find all the function references and imports
        self.visit(self.traversal_file.get_ast())

        # Yield all the references that we are sure are neede, because they were
        # accessed directly off of <module> using dot notation. For example, if
        # we came across <module>.something_that_we_need.
        for function_reference in self.function_references:
            yield function_reference

        # Build a set of all the function names that are imported so that we can
        # check whether a given function call is used in constant time
        imported_function_names = set()
        for function in self.imported_functions:
            imported_function_names.add(function.name)

        # Check all the function calls to see if they are in the imported functions
        for function_name, node in self._possible_references:
            if function_name in imported_function_names:
                # If we find a use, yield it since it is a function reference
                yield ReferencedFunction(function_name, node)

    @keep_visiting
    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "everything":
            for alias in node.names:
                self.imported_functions.add(ReferencedFunction(alias.name, node))
                if alias.asname is not None:
                    self.imported_functions.add(ReferencedFunction(alias.asname, node))

    @keep_visiting
    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self._possible_references.add((node.func.id, node))

    @keep_visiting
    def visit_Attribute(self, node):
        # Find all the attributes of `self.module` that are accessd. For example,
        # if `self.module` is "everything", we would catch everything.example, 
        # everything.another_example(), foo.bar.everything.example(), etc.
        if isinstance(node.value, ast.Name) and node.value.id == self.module:
            self.function_references.add(ReferencedFunction(node.attr, node))


def walk_directory(root_path: Path):
    for file_path in root_path.rglob("*.py"):
        traversal_file = TraversalFile(file_path)
        reference_finder = ModuleFunctionReferenceFinder("everything", traversal_file)
        function_references = reference_finder.find_references()
        for function_reference in function_references:
            print(
                f"Found reference to {function_reference.name} on line {function_reference.line_number} in {file_path}"
            )
