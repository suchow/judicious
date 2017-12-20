# -*- coding: utf-8 -*-

"""Pseudorandom generators for human computation."""

import random

from .core import collect


def joke(person=None):
    """Tell a joke."""
    r = collect("joke", person=person)
    return r['text']


def draw(thing, width=200, height=200, person=None):
    """Draw a thing."""
    r = collect("draw", thing=thing, width=width, height=height, person=person)
    return r['drawing']


def copyedit(text, person=None):
    """Copyedit some text."""
    r = collect("copyedit", text=text, person=person)
    return r['text']


def label(src, person=None):
    """Label an image."""
    r = collect("label", src=src, person=person)
    return r['label']


def identify_letter(letter=None, alphabet=None, lightness=0.80, person=None):
    """Identify a letter in noise."""
    import string

    if not alphabet:
        alphabet = list(string.ascii_lowercase)

    if not letter:
        letter = random.choice(alphabet)

    r = collect(
        "identify_letter",
        letter=letter,
        alphabet=alphabet,
        lightness=lightness,
        person=person
    )
    return (r['letter'], r['letter'] == letter)


def caption(src, person=None):
    """Write a caption for a cartoon."""
    r = collect("caption", src=src, person=person)
    return r['caption']


def select_the(category, src_0, src_1, person=None):
    """Select the image belonging to the category."""
    r = collect(
        "select_the",
        category=category,
        src_0=src_0,
        src_1=src_1,
        person=person,
    )
    return int(r['selection'])


def define(word, person=None):
    """Define the word."""
    r = collect("define", word=word, person=person)
    return r['definition']


def compare_numerosity(a, b, person=None):
    """Determine which numerosity is greater."""
    cb = random.random() > 0.5
    r = collect(
        "compare_numerosity",
        a=a,
        b=b,
        counterbalancer=cb,
        person=person
    )
    return r['selection']


def agree(prompt, person=None):
    """Rate agreement with a prompt."""
    r = collect("agree", prompt=prompt, person=person)
    return r['agreement']


def trolley_problem(person=None):
    """Respond to the trolley problem."""
    r = collect("trolley_problem", person=person)
    return r['decision']


def intertemporal_choice(SS, LL, delay, person=None):
    """Complete an intertemporal choice problem."""
    r = collect(
        "intertemporal_choice",
        SS=SS,
        LL=LL,
        delay=delay,
        person=person
    )
    return r['choice']


def recaptcha(person=None):
    """Solve a reCaptcha."""
    r = collect("recaptcha", person=person)
    return r["solved"]


def chess(
    board="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    person=None
):
    """Take the next move in a game of chess."""
    print(board)
    turn_dict = {
        "b": "black",
        "w": "white"
    }
    turn = turn_dict[board.split(" ")[1]]
    r = collect("chess", board=board, turn=turn, person=person)
    return r["board"]


def noun(person=None):
    """Name a noun."""
    r = collect("noun", person=person)
    return r["word"]


def verb(person=None):
    """Name a verb."""
    r = collect("verb", person=person)
    return r["word"]


def adjective(person=None):
    """Name an adjective."""
    r = collect("adjective", person=person)
    return r["word"]


def summarize(text, max_words=None, person=None):
    """Summarize a text."""
    if not max_words:
        mself, ax_words = len(text.split(" "))
    r = collect("summarize", text=text, max_words=max_words, person=person)
    return r["summary"]


def rank_the(category, srcs, person=None):
    """Rank images according to their resemblance to a category."""
    r = collect(
        "rank_the",
        category=category,
        srcs=srcs,
        person=person,
    )
    return [int(rank) for rank in r["ranks"]]


def more_similar(target, word1, word2, person=None):
    """Which word is more similar to the target?"""
    r = collect(
        "more_similar",
        target=target,
        word1=word1,
        word2=word2,
        person=person
    )
    return r["selection"]


def age(src, person=None):
    """Estimate the age of a person in an image."""
    r = collect("age", src=src, person=person)
    return int(r["age"])


def dimorphism(src, person=None):
    """Rate the gender dimorphism of a person in an image."""
    r = collect("dimorphism", src=src, person=person)
    return int(r["dimorphism"])


def attractiveness(src, person=None):
    """Rate the attractiveness of a person in an image."""
    r = collect("attractiveness", src=src, person=person)
    return int(r["attractiveness"])


def resemblance(src, target, person=None):
    """Rate an image's resemblace to a target person."""
    r = collect("resemblance", src=src, target=target, person=person)
    return int(r["resemblance"])


def reproduce(text, delay=10, person=None):
    """Read some text and then reproduce it verbatim."""
    r = collect("reproduce", text=text, delay=delay, person=person)
    return r["reproduction"]


def spellcheck(text, person=None):
    """Spellcheck some text."""
    r = collect("spellcheck", text=text, person=person)
    return r['text']


def iframe(url, prompt, person=None):
    r = collect("iframe", url=url, prompt=prompt, person=person)
    return r["response"]


def atari(rom):
    r = collect("atari", rom=rom)
    return (r["checkpoints"], r["controls"])


def redact_illicit(scenario, person=None):
    """Redact illicit information from a scenario."""
    r = collect("redact_illicit", scenario=scenario, person=person)
    return r['scenario']
