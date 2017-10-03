# -*- coding: utf-8 -*-

"""Top-level package for judicious."""

__author__ = """Jordan W. Suchow"""
__email__ = 'jwsuchow@gmail.com'
__version__ = '0.1.0'

from .core import (
    base_url,
    collect,
    register,
    seed,
)

from .tasks import (
    copyedit,
    define,
    joke,
    label,
    select_the,
)

__all__ = (
    # Core functions
    "base_url",
    "collect",
    "register",
    "seed",

    # Tasks
    "copyedit",
    "define",
    "joke",
    "label",
    "select_the",
)
