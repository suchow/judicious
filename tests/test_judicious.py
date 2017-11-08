#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `judicious` package."""

import random

import pytest

import judicious


def test_seeding():
    r1 = random.random()
    r2 = random.random()
    judicious.seed("70d911d5-6d93-3c42-f9a4-53e493a79bff")
    r3 = random.random()
    r4 = random.random()
    judicious.seed("70d911d5-6d93-3c42-f9a4-53e493a79bff")
    r5 = random.random()
    r6 = random.random()
    judicious.seed()
    r7 = random.random()
    r8 = random.random()

    assert (r1 != r3)
    assert (r2 != r4)
    assert (r3 == r5)
    assert (r4 == r6)
    assert (r5 != r7)
    assert (r6 != r8)


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
