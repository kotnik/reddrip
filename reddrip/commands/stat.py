""" Running statistics.
"""

import os
import logging

import redis
from texttable import Texttable

from reddrip.commands import Command
from reddrip.util.config import Configuration

log = logging.getLogger(__name__)


class StatCommand(Command):
    """ Get the statistics from Redis.
    """

    help = "Reddrip statistics."

    @classmethod
    def setup_parser(cls, parser):
        parser.add_argument(
            "--config", "-c", help="configuration file", required=True
        )

    def _human_readable(self, size):
        size = float(size)
        sizes = [(1024, "Gb"), (1024, "Mb"), (1024, "Kb"), (1, "b")]
        divider, suffix = sizes.pop()
        while size > 1024:
            try:
                divider, suffix = sizes.pop()
                size = round(size / divider, 2)
            except IndexError:
                break

        return "%s %s" % (size, suffix)

    def execute(self, options):
        conf = Configuration(options.config)

        redis_conn = redis.StrictRedis(
            host=conf.glob["redis.host"],
            port=int(conf.glob["redis.port"]),
            db=conf.glob["redis.db"],
        )

        subreddits = redis_conn.smembers("subreddits")

        print "Total of %d subreddits in database, following %s." % (
            len(subreddits), len(conf)
        )
        print

        table = Texttable(max_width=0)
        table.set_deco(Texttable.HEADER)

        table.header([
            "Name",
            "Type",
            "Processed",
            "Saved",
            "Existing",
            "Size"
        ])
        table.set_cols_align(["l", "l", "r", "r", "r", "r"])

        size = processed = saved = existing = 0
        for subreddit in subreddits:
            try:
                dl_type = conf.subreddit(subreddit)["type"]
            except KeyError:
                continue

            sub_processed = len(
                redis_conn.smembers("stat:%s:processed:all" % subreddit)
            )
            sub_saved = redis_conn.get("stat:%s:saved:count" % subreddit)
            sub_size = redis_conn.get("stat:%s:saved:size" % subreddit)
            subdir = "%s/%s" % (conf.glob["outdir"], subreddit)
            sub_existing = len([
                f for f in os.listdir(subdir)
                if os.path.isfile("%s/%s" % (subdir, f))
            ])

            processed += int(sub_processed)
            saved += int(sub_saved)
            size += int(sub_size)
            existing += sub_existing

            table.add_row([
                subreddit,
                dl_type,
                sub_processed,
                sub_saved,
                sub_existing,
                self._human_readable(sub_size)
            ])

        table.add_row([
            "TOTAL",
            "",
            processed,
            saved,
            existing,
            self._human_readable(size)
        ])

        print table.draw()
