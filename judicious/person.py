import concurrent.futures
import random
import uuid

from . import tasks


class Person(object):
    """A person."""

    def __init__(self):
        self.id = str(uuid.UUID(int=random.getrandbits(128)))

    def __repr__(self):
        return "Person {}".format(self.id)

    def __getattr__(self, name):
        def method(*args, **kwargs):
            try:
                return getattr(tasks, name)(*args, person=self.id, **kwargs)
            except:
                return ''
        return method

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return type in (concurrent.futures.TimeoutError, TimeoutError)
