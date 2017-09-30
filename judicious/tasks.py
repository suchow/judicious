# -*- coding: utf-8 -*-

"""Main module."""

from .core import collect


def joke():
    r = collect("joke")
    return r['text']
