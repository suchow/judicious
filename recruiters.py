"""Recruiters of judicious humans."""

import logging
import os

import boto3

# Set up logging.
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s [recruiter.1]: %(message)s')
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
        logger.info("Recruiting a participant.")


class MTurkRecruiter(Recruiter):
    """Recruits from Amazon Mechanical Turk."""

    def __init__(self):
        self.mode = os.environ["JUDICIOUS_MTURK_MODE"]

        if self.mode == "sandbox":
            self._client = boto3.client(
                service_name='mturk',
                endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com',
            )
        elif self.mode == "live":
            self._client = boto3.client(
                service_name='mturk',
                region_name="us-east-1",
            )

    def _print_balance(self):
        balance = self.client.get_account_balance()['AvailableBalance']
        logger.info("Current MTurk balance is ${}.".format(balance))

    def recruit(self):
        response = self._client.create_hit_with_hit_type(
            HITTypeId=os.environ["JUDICIOUS_MTURK_HIT_TYPE_ID"],
            MaxAssignments=1,
            LifetimeInSeconds=int(os.environ["JUDICIOUS_MTURK_LIFETIME"]),
            Question=open("external.xml", "r").read(),
        )
        logger.info("Created HIT with ID {}".format(response['HIT']['HITId']))
