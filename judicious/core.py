# -*- coding: utf-8 -*-

"""Main module."""

import json
import logging
import multiprocessing as mp
import os
import pickle
import random
import sys
import time
import uuid

import requests

this = sys.modules[__name__]


def generate_uuid():
    """Generate a UUID from pseudorandom bits."""
    return str(uuid.UUID(int=random.getrandbits(128)))


_ctx = None


def context():
    return this._ctx


def seed(s=None):
    """Seed the PRNG."""
    if not s:
        s = generate_uuid()
    random.seed(s)
    global _ctx
    this._ctx = s
    return s


seed()


logger = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("JUDICIOUS_LOG_LEVEL", "INFO"))

CACHE_DIR = os.path.join(os.environ["HOME"], ".local", "share", "judicious")
CACHE_FILEPATH = os.path.join(CACHE_DIR, "cache.pkl")


def unpack_seed_apply(fargseed):
    """Unpack, seed the PRNG, and apply the function."""
    (f, args, seed) = fargseed
    random.seed(seed)
    return f(args)


def map(f, args):
    """Reproducible map with a multiprocessing pool."""
    fs = [f for _ in args]
    seeds = [random.getrandbits(128)+i for i in range(len(args))]
    fargseeds = zip(fs, args, seeds)
    return pool.map(unpack_seed_apply, fargseeds)


def base_url():
    return os.environ.get("JUDICIOUS_URL", "http://imprudent.herokuapp.com")


def register(url):
    """Set the base URL of the decision server."""
    os.environ["JUDICIOUS_URL"] = url


def priority(level=1):
    """Set the priority of new tasks."""
    os.environ["JUDICIOUS_PRIORITY_LEVEL"] = str(level)


def post_task(task_type, task_id=None, parameters={}):
    """Create a new task."""
    if not task_id:
        task_id = generate_uuid()
    person = parameters.pop("person", None)
    return requests.post(
        "{}/tasks/{}".format(base_url(), task_id),
        data={
            'type': task_type,
            'parameters': json.dumps(parameters),
            'priority': os.environ.get("JUDICIOUS_PRIORITY_LEVEL", 1),
            'person': person,
            'context': context(),
        },
    )


def load_cache():
    """Load the cache from disk."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    with open(CACHE_FILEPATH, 'wb+') as f:  # Initialize w/ empty cache.
        pickle.dump({}, f, pickle.HIGHEST_PROTOCOL)

    with open(CACHE_FILEPATH, 'rb') as f:
        return pickle.load(f)


def dump_cache(cache):
    """Dump the cache to disk."""
    with open(CACHE_FILEPATH, 'wb') as f:
        pickle.dump(cache, f, pickle.HIGHEST_PROTOCOL)


def get_task(task_id):
    """Get the result of a task."""
    return requests.get(
        "{}/tasks/{}".format(base_url(), task_id),
    )


def post_result(id, result):
    """Post the result of an existing task."""
    return requests.patch(
        "{}/tasks/{}".format(base_url(), id),
        data={'result': result},
    )


def collect(type, **kwargs):
    """Collect result of a task of the given type."""
    task_id = generate_uuid()

    # Check if the task is in the local cache.
    cache = load_cache()
    if task_id in cache:
        logging.info("Cached result found for {}".format(task_id))
        return cache[task_id]

    while True:
        r = get_task(task_id)

        if r.status_code == 200:
            result = json.loads(r.json()['data']['result'])
            logging.info("Result found for {}".format(task_id))
            logging.info(result)

            # Cache the result.
            cache[task_id] = result
            dump_cache(cache)

            return result

        elif r.status_code == 202:
            logging.info("{} is still in progress".format(task_id))

        elif r.status_code == 404:
            logging.info("Posting {}".format(task_id))
            post_task(type, task_id=task_id, parameters=kwargs)

        else:
            raise Exception("Unknown status code returned")

        time.sleep(1)


pool = mp.Pool(20)  # Create pool last, giving access to everything above.
