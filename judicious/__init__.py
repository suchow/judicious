# -*- coding: utf-8 -*-

"""Top-level package for judicious."""

__author__ = """Jordan W. Suchow"""
__email__ = 'jwsuchow@gmail.com'
__version__ = '0.1.0'

from .core import (
    base_url,
    collect,
    priority,
    register,
    seed,
)

from .tasks import (
    adjective,
    age,
    agree,
    chess,
    compare_numerosity,
    copyedit,
    define,
    dimorphism,
    intertemporal_choice,
    joke,
    label,
    noun,
    recaptcha,
    select_the,
    summarize,
    trolley_problem,
    verb,
)

__all__ = (
    # Core functions
    "base_url",
    "collect",
    "priority",
    "register",
    "seed",

    # Tasks
    "adjective",
    "age",
    "agree",
    "chess",
    "compare_numerosity",
    "copyedit",
    "define",
    "dimorphism",
    "intertemporal_choice",
    "joke",
    "label",
    "noun",
    "recaptcha",
    "select_the",
    "summarize",
    "trolley_problem",
    "verb",
)
