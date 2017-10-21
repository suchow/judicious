# -*- coding: utf-8 -*-

"""Top-level package for judicious."""

__author__ = """Jordan W. Suchow"""
__email__ = 'jwsuchow@gmail.com'
__version__ = '0.1.0'

from .core import (
    base_url,
    collect,
    map,
    priority,
    register,
    seed,
    unpack_seed_apply,
)

from .tasks import (
    adjective,
    age,
    agree,
    attractiveness,
    chess,
    compare_numerosity,
    copyedit,
    define,
    dimorphism,
    intertemporal_choice,
    joke,
    label,
    noun,
    rank_the,
    recaptcha,
    resemblance,
    select_the,
    summarize,
    trolley_problem,
    verb,
)

from . import tasks

from .person import Person

__all__ = (
    # Core functions
    "base_url",
    "collect",
    "map",
    "Person",
    "priority",
    "register",
    "seed",
    "tasks",
    "unpack_seed_apply",

    # Tasks
    "adjective",
    "age",
    "agree",
    "attractiveness",
    "chess",
    "compare_numerosity",
    "copyedit",
    "define",
    "dimorphism",
    "intertemporal_choice",
    "joke",
    "label",
    "noun",
    "rank_the",
    "recaptcha",
    "resemblance",
    "select_the",
    "summarize",
    "trolley_problem",
    "verb",
)
