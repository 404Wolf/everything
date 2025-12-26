from everything.utils.misc import (
    extract_from_codeblock_if_in_codeblock,
    str_function_to_real_function,
    extract_inner_content_from_function,
)


def test_extract_from_codeblock_if_in_codeblock():
    plain_code = "def foo():\n    pass"
    result = extract_from_codeblock_if_in_codeblock(plain_code)
    assert result == plain_code

    multiline = """```python
import os

def bar(x, y):
    return x + y
```"""
    result = extract_from_codeblock_if_in_codeblock(multiline)
    assert result == "import os\n\ndef bar(x, y):\n    return x + y"


def test_str_function_to_real_function():
    code = """def add(a, b):
    return a + b"""
    func = str_function_to_real_function(code)
    assert func(2, 3) == 5
    assert func(10, -5) == 5


def test_extract_inner_content_from_function():
    code = """def calculate(x, y):
    if x > y:
        result = x - y
    else:
        result = y - x
    return result"""
    result = extract_inner_content_from_function(code)
    expected = """if x > y:
    result = x - y
else:
    result = y - x
return result"""
    assert result == expected
