""" Run reddrip.
"""

import logging

import redis

from reddrip.commands import Command
from reddrip.util.config import Configuration
from reddrip.ripper import Ripper

log = logging.getLogger(__name__)


class RunCommand(Command):
    """ Main command, used to run reddrip.
    """

    help = "Reddrip runner."

    @classmethod
    def setup_parser(cls, parser):
        parser.add_argument(
            "--config", "-c", help="configuration file", required=True
        )

    def execute(self, options):
        log.info("Starting reddrip")

        conf = Configuration(options.config)

        redis_conn = redis.StrictRedis(
            host=conf.glob["redis.host"],
            port=int(conf.glob["redis.port"]),
            db=conf.glob["redis.db"],
        )

        rip = Ripper(redis_conn, conf.glob["outdir"])

        # Main runner.
        while True:
            conf.read()
            for subreddit in conf.subreddits():
                rip.process(subreddit)
