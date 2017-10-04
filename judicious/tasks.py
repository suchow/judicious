# -*- coding: utf-8 -*-

"""Pseudorandom generators for human computation."""

import random

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


def define(word):
    r = collect("define", word=word)
    return r['definition']


def compare_numerosity(a, b):
    cb = random.random() > 0.5
    r = collect("compare_numerosity", a=a, b=b, counterbalancer=cb)
    return r['selection']
