from pathlib import Path

from everything.utils.scanner import walk_directory

def main():
    root = Path.cwd()
    walk_directory(root / "temp")

if __name__ == "__main__":
    pass

