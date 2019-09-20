import random
import time
import uuid

import requests

import judicious

# BASE_URL = "http://imprudent.herokuapp.com"
BASE_URL = "http://127.0.0.1:5000"

judicious.register(BASE_URL)


def generate_uuid():
    """Generate a UUID from pseudorandom bits."""
    return str(uuid.UUID(int=random.getrandbits(128)))


def post_task(task_type, task_id=None):
    """Create a new task."""
    if not task_id:
        task_id = generate_uuid()
    return requests.post(
        "{}/tasks/{}".format(BASE_URL, task_id),
        data={'type': task_type},
    )


def get_task(id):
    """Get the result of an existing task."""
    return requests.get("{}/tasks/{}".format(BASE_URL, id), )


def post_result(id, result):
    """Post the result of an existing task."""
    return requests.patch(
        "{}/tasks/{}".format(BASE_URL, id),
        data={'result': result},
    )


def collect(type):
    """Collect results of a task of the given type."""
    task_id = generate_uuid()
    r = get_task(task_id)
    if r.status_code == 200:
        return r.json()['data']['result']

    elif r.status_code == 404:
        post_task("joke", task_id=task_id)

    while r.status_code != 200:
        time.sleep(1)
        r = get_task(task_id)

    return r.json()['data']['result']


r = collect("joke")
