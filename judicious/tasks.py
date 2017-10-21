# -*- coding: utf-8 -*-

"""Pseudorandom generators for human computation."""

import random

from .core import collect


class Task(object):
    """A callable task."""
    def __init__(self, *args, **kwargs):
        self.person = kwargs.get("person")
        self.__call__()

    def collect(self, *args, **kwargs):
        return collect(*args, person=self.person, **kwargs)

    def __call__(self):
        raise NotImplementedError


class joke(Task):
    """Tell a joke."""
    def __call__(self):
        r = self.collect("joke")
        return r['text']


class copyedit(Task):
    """Copyedit some text."""
    def __call__(self, text):
        r = self.collect("copyedit", text=text)
        return r['text']


class label(Task):
    """Label an image."""
    def __call__(self, src):
        r = self.collect("label", src=src)
        return r['label']


class select_the(Task):
    """Select the image belonging to the category."""
    def __call__(self, category, src_0, src_1):
        r = self.collect(
            "select_the",
            category=category,
            src_0=src_0,
            src_1=src_1
        )
        return r['selection']


class define(Task):
    """Define the word."""
    def __call__(self, word):
        r = self.collect("define", word=word)
        return r['definition']


class compare_numerosity(Task):
    """Determine which numerosity is greater."""
    def __call__(self, a, b):
        cb = random.random() > 0.5
        r = self.collect("compare_numerosity", a=a, b=b, counterbalancer=cb)
        return r['selection']


class agree(Task):
    """Rate agreement with a prompt."""
    def __call__(self, prompt):
        r = self.collect("agree", prompt=prompt)
        return r['agreement']


class trolley_problem(Task):
    """Respond to the trolley problem."""
    def __call__(self):
        r = self.collect("trolley_problem")
        return r['decision']


class intertemporal_choice(Task):
    """Complete an intertemporal choice problem."""
    def __call__(self, SS, LL, delay):
        r = self.collect("intertemporal_choice", SS=SS, LL=LL, delay=delay)
        return r['choice']


class recaptcha(Task):
    """Solve a reCaptcha."""
    def __call__(self):
        r = self.collect("recaptcha")
        return r["solved"]


class chess(Task):
    """Take the next move in a game of chess."""
    starting_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __call__(self, board=starting_board):
        turn_dict = {
            "b": "black",
            "w": "white"
        }
        turn = turn_dict[board.split(" ")[1]]
        r = self.collect("chess", board=board, turn=turn)
        return r["board"]


class noun(Task):
    """Name a noun."""
    def __call__(self):
        r = self.collect("noun")
        return r["word"]


class verb(Task):
    """Name a verb."""
    def __call__(self):
        r = self.collect("verb")
        return r["word"]


class adjective(Task):
    """Name an adjective."""
    def __call__(self):
        r = self.collect("adjective")
        return r["word"]


class summarize(Task):
    """Summarize a text."""
    def __call__(self, text, max_words=None):
        if not max_words:
            mself, ax_words = len(text.split(" "))
        r = self.collect("summarize", text=text, max_words=max_words)
        return r["summary"]

class rank_the(Task):
    """Rank images according to their resemblance to a category."""
    def __call__(self, category, srcs):
        r = self.collect(
            "rank_the",
            category=category,
            srcs=srcs,
        )
        return [int(rank) for rank in r["ranks"]]


class age(Task):
    """Estimate the age of a person in an image."""
    def __call__(self, src):
        r = self.collect("age", src=src)
        return int(r["age"])


class dimorphism(Task):
    """Rate the gender dimorphism of a person in an image."""
    def __call__(self, src):
        r = self.collect("dimorphism", src=src)
        return int(r["dimorphism"])


class attractiveness(Task):
    """Rate the attractiveness of a person in an image."""
    def __call__(self, src):
        r = self.collect("attractiveness", src=src)
        return int(r["attractiveness"])


class resemblance(Task):
    """Rate an image's resemblace to a target person."""
    def __call__(self, src, target):
        r = self.collect("resemblance", src=src, target=target)
        return int(r["resemblance"])
