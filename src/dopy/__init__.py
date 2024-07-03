"""Top-level package for DoPy."""

__author__ = """Wolf Mermelstein"""
__email__ = "wolfmermelstein@gmail.com"
__version__ = "0.1.0"


def __getattr__(name: str):
    from .makethething import make_the_thing

    return make_the_thing(name)
