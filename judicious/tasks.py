# -*- coding: utf-8 -*-

"""Pseudorandom generators for human computation."""

import os
import random
import uuid

from .core import collect, map


def consent(
    title=None,
    body=None,
    prompt=None,
    agree=None,
    disagree=None,
    **kwargs
):
    if not title:
        title = "Consent to participate in research"
    if not body:
        consent_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "consent_body.html"
        )
        with open(consent_path, "r") as f:
            body = f.read()
    if not prompt:
        prompt = "Do you understand and agree to participate?"
    if not agree:
        agree = "I agree"
    if not disagree:
        disagree = "No thanks (Exit)"

    r = collect(
        "consent",
        title=title,
        body=body,
        prompt=prompt,
        agree=agree,
        disagree=disagree,
        **kwargs
    )
    return r["consent"]


def judge_face(face, attribute, **kwargs):
    r = collect("judge_face", face=face, attribute=attribute, **kwargs)
    return r


def instruct_judge_faces(**kwargs):
    """Give instructions for rating faces."""
    collect("instruct_judge_faces", **kwargs)


def attrition(**kwargs):
    """Affirm the anti-attrition statement."""
    r = collect("attrition", **kwargs)
    return r['attrition']


def debrief(**kwargs):
    """Complete a debriefing survey."""
    r = collect("debrief", **kwargs)
    return r


def complete(**kwargs):
    """Tell the participant that they are all done."""
    r = collect("complete", **kwargs)
    return r['complete']


def joke(**kwargs):
    """Tell a joke."""
    r = collect("joke", **kwargs)
    return r['text']


def draw(thing, width=200, height=200, **kwargs):
    """Draw a thing."""
    r = collect("draw", thing=thing, width=width, height=height, **kwargs)
    return r['drawing']


def copyedit(text, **kwargs):
    """Copyedit some text."""
    r = collect("copyedit", text=text, **kwargs)
    return r['text']


def label(src, **kwargs):
    """Label an image."""
    r = collect("label", src=src, **kwargs)
    return r['label']


def identify_letter(letter=None, alphabet=None, lightness=0.80, **kwargs):
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
        **kwargs
    )
    return (r['letter'], r['letter'] == letter)


def caption(src, **kwargs):
    """Write a caption for a cartoon."""
    r = collect("caption", src=src, **kwargs)
    return r['caption']


def select_the(category, src_0, src_1, **kwargs):
    """Select the image belonging to the category."""
    r = collect(
        "select_the",
        category=category,
        src_0=src_0,
        src_1=src_1,
        **kwargs
    )
    return int(r['selection'])


def select_the_stick_animal(category, animal_0, animal_1, **kwargs):
    """Select the stick figure that matches the category."""
    r = collect(
        "select_the_stick_animal",
        category=category,
        animal_0=animal_0,
        animal_1=animal_1,
        **kwargs
    )
    return int(r['selection'])


def define(word, **kwargs):
    """Define the word."""
    r = collect("define", word=word, **kwargs)
    return r['definition']


def compare_numerosity(a, b, **kwargs):
    """Determine which numerosity is greater."""
    cb = random.random() > 0.5
    r = collect(
        "compare_numerosity",
        a=a,
        b=b,
        counterbalancer=cb,
        **kwargs
    )
    return r['selection']


def agree(prompt, **kwargs):
    """Rate agreement with a prompt."""
    r = collect("agree", prompt=prompt, **kwargs)
    return r['agreement']


def trolley_problem(**kwargs):
    """Respond to the trolley problem."""
    r = collect("trolley_problem", **kwargs)
    return r['decision']


def intertemporal_choice(SS, LL, delay, **kwargs):
    """Complete an intertemporal choice problem."""
    r = collect(
        "intertemporal_choice",
        SS=SS,
        LL=LL,
        delay=delay,
        **kwargs
    )
    return r['choice']


def recaptcha(**kwargs):
    """Solve a reCaptcha."""
    r = collect("recaptcha", **kwargs)
    return r["solved"]


def chess(
    board="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    **kwargs
):
    """Take the next move in a game of chess."""
    print(board)
    turn_dict = {
        "b": "black",
        "w": "white"
    }
    turn = turn_dict[board.split(" ")[1]]
    r = collect("chess", board=board, turn=turn, **kwargs)
    return r["board"]


def noun(**kwargs):
    """Name a noun."""
    r = collect("noun", **kwargs)
    return r["word"]


def verb(**kwargs):
    """Name a verb."""
    r = collect("verb", **kwargs)
    return r["word"]


def adjective(**kwargs):
    """Name an adjective."""
    r = collect("adjective", **kwargs)
    return r["word"]


def summarize(text, max_words=None, **kwargs):
    """Summarize a text."""
    if not max_words:
        mself, ax_words = len(text.split(" "))
    r = collect("summarize", text=text, max_words=max_words, **kwargs)
    return r["summary"]


def rank_the(category, srcs, **kwargs):
    """Rank images according to their resemblance to a category."""
    r = collect(
        "rank_the",
        category=category,
        srcs=srcs,
        **kwargs
    )
    return [int(rank) for rank in r["ranks"]]


def more_similar(target, word1, word2, **kwargs):
    """Which word is more similar to the target?"""
    r = collect(
        "more_similar",
        target=target,
        word1=word1,
        word2=word2,
        **kwargs
    )
    return r["selection"]


def age(src, **kwargs):
    """Estimate the age of a person in an image."""
    r = collect("age", src=src, **kwargs)
    return int(r["age"])


def dimorphism(src, **kwargs):
    """Rate the gender dimorphism of a person in an image."""
    r = collect("dimorphism", src=src, **kwargs)
    return int(r["dimorphism"])


def attractiveness(src, **kwargs):
    """Rate the attractiveness of a person in an image."""
    r = collect("attractiveness", src=src, **kwargs)
    return int(r["attractiveness"])


def resemblance(src, target, **kwargs):
    """Rate an image's resemblace to a target person."""
    r = collect("resemblance", src=src, target=target, **kwargs)
    return int(r["resemblance"])


def reproduce(text, delay=10, **kwargs):
    """Read some text and then reproduce it verbatim."""
    r = collect("reproduce", text=text, delay=delay, **kwargs)
    return r["reproduction"]


def spellcheck(text, **kwargs):
    """Spellcheck some text."""
    r = collect("spellcheck", text=text, **kwargs)
    return r['text']


def channel(prompt, channel=None):
    """Visit a channel."""
    if not channel:
        channel = str(uuid.uuid4())
    from faker import Factory
    fake = Factory.create("en_US")
    profile = fake.simple_profile()
    r = collect(
        "channel",
        prompt=prompt,
        pseudonym=profile['name'],
        channel=channel
    )
    return r["transcript"]


def chat(prompt, N=3):
    ch = str(uuid.uuid4())
    transcripts = map(channel, [(prompt, ch) for _ in range(N)])
    return {
        "transcript": sorted([i for sub in transcripts for i in sub]),
    }


def iframe(url, prompt, **kwargs):
    r = collect("iframe", url=url, prompt=prompt, **kwargs)
    return r["response"]


def atari(rom):
    r = collect("atari", rom=rom)
    return (r["checkpoints"], r["controls"])


def redact_illicit(scenario, **kwargs):
    """Redact illicit information from a scenario."""
    r = collect("redact_illicit", scenario=scenario, **kwargs)
    return r['scenario']


def build_tower(prompt, **kwargs):
    """Build a tower that meets the requirements of the prompt."""
    r = collect("build_tower", prompt=prompt, **kwargs)
    return r['tower']


def risky_choice(PA1, A1, A2, PB1, B1, B2, **kwargs):
    """Choose between two risky alternatives."""
    r = collect("risky_choice", PA1=PA1, A1=A1, A2=A2, PB1=PB1, B1=B1, B2=B2)
    print(r)
    return r['choice']


def risky_choice_tools(PA1, A1, A2, PB1, B1, B2, **kwargs):
    """Choose between two risky alternatives in the context of tool use."""
    r = collect("risky_choice_tools", PA1=PA1, A1=A1, A2=A2, PB1=PB1, B1=B1, B2=B2)
    print(r)
    return r['choice']
def match_faces_feedback(faceA, faceB, **kwargs):
    """Determine whether two faces are the same person."""
    r = collect("match_faces_feedback", face_A_src=faceA, face_B_src=faceB, **kwargs)
    return r['match']

def match_faces_no_feedback(faceA, faceB, **kwargs):
    """Determine whether two faces are the same person."""
    r = collect("match_faces_no_feedback", face_A_src=faceA, face_B_src=faceB, **kwargs)
    return r['match']

def multiply(number1, number2, **kwargs):
    """Simple multipication"""
    r = collect("multiply", math_input=number1, math_input2=number2, **kwargs)
    return int(r['math_answer'])
