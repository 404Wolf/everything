"""Top-level package for DoPy."""

__author__ = """Wolf Mermelstein"""
__email__ = "wolfmermelstein@gmail.com"
__version__ = "0.1.0"


from typing import Callable
from everything.generator import runtime_generate_function


def __getattr__(name: str) -> Callable:
    return runtime_generate_function(name)
