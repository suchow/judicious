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
    atari,
    attractiveness,
    attrition,
    build_tower,
    caption,
    channel,
    chat,
    chess,
    compare_numerosity,
    copyedit,
    debrief,
    define,
    dimorphism,
    draw,
    identify_letter,
    iframe,
    intertemporal_choice,
    instruct_judge_faces,
    joke,
    judge_face,
    label,
    more_similar,
    noun,
    rank_the,
    recaptcha,
    redact_illicit,
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
    "atari",
    "attractiveness",
    "attrition",
    "build_tower",
    "caption",
    "channel",
    "chat",
    "chess",
    "compare_numerosity",
    "copyedit",
    "debrief",
    "define",
    "dimorphism",
    "draw",
    "identify_letter",
    "iframe",
    "instruct_judge_faces",
    "intertemporal_choice",
    "joke",
    "judge_face",
    "label",
    "more_similar",
    "noun",
    "rank_the",
    "recaptcha",
    "redact_illicit",
    "reproduce",
    "resemblance",
    "select_the",
    "spellcheck",
    "summarize",
    "trolley_problem",
    "verb",
)
