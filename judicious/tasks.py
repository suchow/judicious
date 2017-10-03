# -*- coding: utf-8 -*-

"""Pseudorandom generators for human computation."""

from .core import collect


def joke():
    r = collect("joke")
    return r['text']


def copyedit(text):
    r = collect("copyedit", text=text)
    return r['text']


def label(src):
    r = collect("label", src=src)
    return r['label']


def select_the(category, src_0, src_1):
    r = collect("select_the", category=category, src_0=src_0, src_1=src_1)
    return r['selection']
