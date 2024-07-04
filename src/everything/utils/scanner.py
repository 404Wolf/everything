import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FunctionToGenerate:
    name: str
    arguments: list[ast.AST]
    keyword_arguments: list[ast.AST]


def process_file(filepath: Path) -> ast.AST:
    with filepath.open("r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
    return tree


def get_context(path: Path, line: int, radius: int = 4):
    lines = path.read_text().split("\n")
    start_line = max(0, line - radius)
    end_line = min(len(lines), line + radius)
    return "\n".join(lines[start_line:end_line])


def walk_directory(root_path: Path):
    needs_to_be_generated = []
    for file_path in root_path.rglob("*.py"):
        tree = process_file(file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "everything":
                needs_to_be_generated.extend((name.name for name in node.names))
            if isinstance(node, ast.Call):
                node_id = node.func.id if hasattr(node.func, "id") else node.func.attr
                if hasattr(node.func, "value") and node.func.value.id == "everything":
                    line_content = get_context(file_path, node.lineno)
                    print(line_content)
                    needs_to_be_generated.append(
                        FunctionToGenerate(node_id, node.args, node.keywords)
                    )
    print(needs_to_be_generated)
