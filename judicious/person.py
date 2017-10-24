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
            return getattr(tasks, name)(*args, person=self.id, **kwargs)
        return method
