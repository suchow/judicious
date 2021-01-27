# -*- coding: utf-8 -*-

"""Top-level package for judicious."""

__author__ = """Jordan W. Suchow"""
__email__ = 'jwsuchow@gmail.com'
__version__ = '0.1.0'

import os


with open(".JUDICIOUS_SERVER_URL", "w") as f:
    url = os.environ.get("JUDICIOUS_SERVER_URL", "http://127.0.0.1:5000")
    f.write(url)


from .core import (
    base_url,
    collect,
    context,
    map,
    map2,
    map3,
    priority,
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
    complete,
    consent,
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
    risky_choice,
    risky_choice_tools,
    select_the,
    spellcheck,
    summarize,
    trolley_problem,
    verb,
    multiply,
    match_faces_feedback,
    match_faces_no_feedback,
    matching_confidence_with_cause,
    matching_confidence,
)

from . import tasks

from .person import Person


__all__ = (
    # Core functions
    "base_url",
    "collect",
    "context",
    "map",
    "map2",
    "map3",
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
    "complete",
    "consent",
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
    "risky_choice",
    "risky_choice_tools",
    "select_the",
    "spellcheck",
    "summarize",
    "trolley_problem",
    "verb",
    "multiply",
    "match_faces_feedback",
    "match_faces_no_feedback",
    "matching_confidence_with_cause",
    "matching_confidence",
)
