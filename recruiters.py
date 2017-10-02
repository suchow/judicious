"""Recruiters of judicious humans."""

import logging

# Set up logging.
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s [clock.1]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Recruiter(object):
    """Generic recruiter."""

    def recruit(self):
        raise NotImplementedError


class HotAirRecruiter(Recruiter):
    """Talks about recruiting, but does not recruit."""

    def recruit(self):
        logger.info("Recruiting a new participant...")


class MTurkRecruiter(Recruiter):
    """Recruits from Amazon Mechanical Turk."""

    def recruit(self):
        raise NotImplementedError
