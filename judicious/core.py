# -*- coding: utf-8 -*-

"""Main module."""

from concurrent.futures import TimeoutError
import datetime
import json
import logging
import multiprocessing as mp
import os
import pickle
import random
import time
import uuid

from dateutil.parser import parse
import pebble
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("JUDICIOUS_LOG_LEVEL", "INFO"))

CACHE_DIR = os.path.join(os.environ["HOME"], ".local", "share", "judicious")
CACHE_FILEPATH = os.path.join(CACHE_DIR, "cache.pkl")


def generate_uuid():
    """Generate a UUID from pseudorandom bits."""
    return uuid.UUID(int=random.getrandbits(128))


_ctx = None


def context():
    global _ctx
    return _ctx


def seed(s=None):
    """Seed the PRNG."""
    if not s:
        s = str(generate_uuid())
    random.seed(s)
    logging.info("Seeding with {}".format(s))
    try:
        import numpy as np
        np.random.seed(int(uuid.UUID(s)) % (2**32 - 1))
    except ImportError:
        pass
    global _ctx
    _ctx = s
    return s


seed()


def unpack_seed_apply(fargseed):
    """Unpack, seed the PRNG, and apply the function."""
    (f, args, seed) = fargseed
    random.seed(seed)
    if not args:
        return f()
    else:
        return f(*args)


def map(f, args):
    """Reproducible map with a multiprocessing pool."""
    fs = [f for _ in args]
    seeds = [random.getrandbits(128) for _ in args]
    fargseeds = zip(fs, args, seeds)
    return pool.map(unpack_seed_apply, fargseeds)


def map2(f, args, timeout=None):
    """Reproducible map with Pebble multiprocessing tool.

    Return all results that finish before timeout, None otherwise."""
    fs = [f for _ in args]
    seeds = [random.getrandbits(128) for _ in args]
    fargseeds = zip(fs, args, seeds)
    pool = pebble.ProcessPool()
    future = pool.map(unpack_seed_apply, fargseeds)
    iterator = future.result()
    results = []
    while True:
        try:
            result = next(iterator)
            results.append(result)
        except StopIteration:
            break
        except pebble.ProcessExpired as error:
            print("%s. Exit code: %d" % (error, error.exitcode))

    return results


def map3(f, args):
    """Reproducible map with Pebble multiprocessing tool.

    Restart any slots that time out, always returning a non-None value."""
    results = [None for _ in range(len(args))]
    while None in results:
        todo_idxs = [i for i, x in enumerate(results) if x is None]
        todo_args = [args[i] for i in todo_idxs]
        partial_results = map2(f, todo_args)
        for i, idx in enumerate(todo_idxs):
            if partial_results[i] is not None:
                results[idx] = partial_results[i]
    return results


def base_url():
    with open(".JUDICIOUS_SERVER_URL", "r") as f:
        url = f.read()
        if url:
            return url
    return os.environ.get(
        "JUDICIOUS_SERVER_URL", "https://imprudent.herokuapp.com")


def register(url):
    """Set the base URL of the decision server."""
    os.environ["JUDICIOUS_SERVER_URL"] = url
    with open(".JUDICIOUS_SERVER_URL", "w") as f:
        f.write(url)


def priority(level=1):
    """Set the priority of new tasks."""
    os.environ["JUDICIOUS_PRIORITY_LEVEL"] = str(level)


def post_task(task_type, task_id=None, parameters={}):
    """Create a new task."""
    if not task_id:
        task_id = str(generate_uuid())
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

    if not os.path.exists(CACHE_FILEPATH):  # Initialize w/ empty cache.
        with open(CACHE_FILEPATH, 'wb+') as f:
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


def get_person(person_id):
    """Get the person."""
    return requests.get(
        "{}/persons/{}".format(base_url(), person_id)
    )


def elapsed_time(person_id):
    """Get the time elapsed since a Person was claimed."""
    r = get_person()
    if r.status_code == 200:
        claimed_at = r.json()['data']['claimed_at']
        server_now = r.json()['data']['now']
        if not claimed_at:
            return 0
        else:
            return (parse(server_now) - parse(claimed_at)).total_seconds()
    elif r.status_code == 404:
        return False
    else:
        raise RuntimeError


def expired(person_id, lifetime):
    """Was the person claimed earlier than their lifetime ago?"""
    return person_id and (elapsed_time(person_id) > lifetime)


def post_result(id, result):
    """Post the result of an existing task."""
    return requests.patch(
        "{}/tasks/{}".format(base_url(), id),
        data={'result': result},
    )


def collect(type, **kwargs):
    """Collect result of a task of the given type."""
    task_id = str(generate_uuid())

    # Check if the task is in the local cache.
    cache = load_cache()
    if task_id in cache:
        logging.info("Cached result found for {}".format(task_id))
        return cache[task_id]

    # Get Person associated with task, if any.
    person_id = kwargs.get('person', None)
    lifetime = kwargs.get('lifetime', None)

    while True:

        r = get_task(task_id)

        if r.status_code == 200:  # A result was found

            if person_id:
                finished_at = parse(r.json()['data']['finished_at'])
                claimed_at = parse(get_person(person_id).json()['data']['claimed_at'])
                if (finished_at - claimed_at).total_seconds() > lifetime:
                    logging.info("Result for {} submitted {} s after expiration".format(task_id, (finished_at - claimed_at).total_seconds()))
                    raise TimeoutError

            result = r.json()['data']['result']
            logging.info("Result found for {}".format(task_id))
            logging.info(result)

            # Cache the result.
            cache[task_id] = result
            dump_cache(cache)

            return result

        elif r.status_code == 202:  # Task is outstanding
            if expired(person_id, lifetime):
                raise TimeoutError
            else:
                logging.info("{} is still in progress".format(task_id))
                pass

        elif r.status_code == 404:  # Task does not exist
            if expired(person_id, lifetime):
                raise TimeoutError
            else:
                logging.info("Posting {}".format(task_id))
                post_task(type, task_id=task_id, parameters=kwargs)

        else:
            raise Exception("Unknown status code returned")

        time.sleep(1)


pool = mp.Pool(20)  # Create pool last, giving access to everything above.
