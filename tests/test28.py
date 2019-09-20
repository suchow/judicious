import judicious

judicious.register("http://127.0.0.1:5000")


class Task(object):

    """A callable task."""

    def __init__(self, *args, **kwargs):
        self.person = kwargs.get("person")

    def collect(self, *args, **kwargs):
        judicious.collect(*args, person=self.person, **kwargs)

    def __call__(self):
        raise NotImplementedError


joke = Task()
joke()


class joke(Task):

    """docstring for joke."""

    def __call__(self):
        raise NotImplementedError
