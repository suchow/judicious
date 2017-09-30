# -*- coding: utf-8 -*-

"""Pseudorandom generators for human computation."""

from .core import collect


def joke():
    r = collect("joke")
    return r['text']
