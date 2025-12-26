import tempfile
from pathlib import Path

from inline_snapshot import snapshot

from everything.utils.scanner import build_context_strings


def test_build_context_strings():
    """Test that build_context_strings generates example usage strings correctly"""

    with tempfile.TemporaryDirectory() as tmp_path:
        tmp_path = Path(tmp_path)

        file1 = tmp_path / "test1.py"
        _ = file1.write_text(
            """from everything import foo
x = 1
foo()
y = 2
"""
        )

        file2 = tmp_path / "test2.py"
        _ = file2.write_text(
            """from everything import foo, bar
a = 1
foo(123)
bar("hello")
b = 2
"""
        )

        context_strings = build_context_strings(tmp_path, "everything", radius=2)

        assert context_strings["foo"] == snapshot(
            """\
# Example Usage:
```py (test1.py:3)
x = 1
foo()
y = 2

```
```py (test2.py:3)
a = 1
foo(123)
bar("hello")
b = 2
```
"""
        )

        assert context_strings["bar"] == snapshot(
            """\
# Example Usage:
```py (test2.py:4)
foo(123)
bar("hello")
b = 2

```
"""
        )
