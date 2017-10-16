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


def agree(prompt):
    r = collect("agree", prompt=prompt)
    return r['agreement']


def trolley_problem():
    r = collect("trolley_problem")
    return r['decision']


def intertemporal_choice(SS, LL, delay):
    r = collect("intertemporal_choice", SS=SS, LL=LL, delay=delay)
    return r['choice']


def recaptcha():
    r = collect("recaptcha")
    return r["solved"]


def chess(board="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    turn_dict = {
        "b": "black",
        "w": "white"
    }
    turn = turn_dict[board.split(" ")[1]]
    r = collect("chess", board=board, turn=turn)
    return r["board"]


def noun():
    r = collect("noun")
    return r["word"]


def verb():
    r = collect("verb")
    return r["word"]


def adjective():
    r = collect("adjective")
    return r["word"]


def summarize(text, max_words=None):
    if not max_words:
        max_words = len(text.split(" "))
    r = collect("summarize", text=text, max_words=max_words)
    return r["summary"]


def age(src):
    r = collect("age", src=src)
    return r["age"]
