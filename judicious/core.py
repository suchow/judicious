# -*- coding: utf-8 -*-

"""Main module."""

from datetime import timedelta
import json
import os
import random
import time
import uuid

import requests


def base_url():
    return os.environ.get("JUDICIOUS_URL", "http://imprudent.herokuapp.com")


def register(url):
    """Set the base URL of the decision server."""
    os.environ["JUDICIOUS_URL"] = url


def priority(level=1):
    """Set the priority of new tasks."""
    os.environ["JUDICIOUS_PRIORITY_LEVEL"] = str(level)


def seed(s):
    """Seed the PRNG."""
    random.seed(s)


def generate_id():
    """Generate a UUID from pseudorandom bits."""
    return str(uuid.UUID(int=random.getrandbits(128)))


def post_task(task_type, task_id=None, parameters={}):
    """Create a new task."""
    if not task_id:
        task_id = generate_id()
    return requests.post(
        "{}/tasks/{}".format(base_url(), task_id),
        data={
            'type': task_type,
            'parameters': json.dumps(parameters),
            'priority': os.environ.get("JUDICIOUS_PRIORITY_LEVEL", 1),
        },
    )


def get_task(id):
    """Get the result of an existing task."""
    return requests.get(
        "{}/tasks/{}".format(base_url(), id),
    )


def post_result(id, result):
    """Post the result of an existing task."""
    return requests.patch(
        "{}/tasks/{}".format(base_url(), id),
        data={'result': result},
    )


def collect(type, **kwargs):
    """Collect result of a task of the given type."""
    task_id = generate_id()
    r = get_task(task_id)
    if r.status_code == 200:
        return json.loads(r.json()['data']['result'])

    elif r.status_code == 404:
        post_task(type, task_id=task_id, parameters=kwargs)

    while r.status_code != 200:
        time.sleep(1)
        r = get_task(task_id)

    return json.loads(r.json()['data']['result'])
