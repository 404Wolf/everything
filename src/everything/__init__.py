"""Top-level package for everything.py."""

import os
import logging
from typing import Callable
from dotenv import load_dotenv

__author__ = """Wolf Mermelstein"""
__email__ = "wolf@404wolf.com"


load_dotenv()
from everything.generator import (  # noqa: E402
    runtime_generate_function,
)  # (need env var set to import)

# Setup logger if env var set
if os.getenv("EVERYTHING_DEBUG", "0") == "1":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.debug("Debug logging enabled for everything.py")


def __getattr__(name: str) -> Callable:
    return runtime_generate_function(name)
