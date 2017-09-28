# -*- coding: utf-8 -*-

"""Main module."""

import os
import uuid

import requests

BASE_URL = os.environ.get("JUDICIOUS_URL", "http://imprudent.herokuapp.com")

UUID = str(uuid.uuid4())


def register(url):
    """Set the base URL of the decision server."""
    os.environ["JUDICIOUS_URL"] = url

