# -*- coding: utf-8 -*-

"""Top-level package for judicious."""

__author__ = """Jordan W. Suchow"""
__email__ = 'jwsuchow@gmail.com'
__version__ = '0.1.0'

import os

from .core import (
    base_url,
    collect,
    context,
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
    caption,
    chess,
    compare_numerosity,
    copyedit,
    define,
    dimorphism,
    draw,
    intertemporal_choice,
    joke,
    label,
    noun,
    rank_the,
    recaptcha,
    reproduce,
    resemblance,
    select_the,
    spellcheck,
    summarize,
    trolley_problem,
    verb,
)

from . import tasks

from .person import Person

register(os.environ.get("JUDICIOUS_SERVER_URL", "http://127.0.0.1:5000"))


__all__ = (
    # Core functions
    "base_url",
    "collect",
    "context",
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
    "caption",
    "chess",
    "compare_numerosity",
    "copyedit",
    "define",
    "dimorphism",
    "draw",
    "intertemporal_choice",
    "joke",
    "label",
    "noun",
    "rank_the",
    "recaptcha",
    "reproduce",
    "resemblance",
    "select_the",
    "spellcheck",
    "summarize",
    "trolley_problem",
    "verb",
)
