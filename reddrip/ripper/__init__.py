import os
import logging
import time
import re
import urlparse

from redis.exceptions import ResponseError
import requests
import praw

log = logging.getLogger(__name__)


class Ripper(object):

    timeout = 40
    agent = "Reddrip v1.0"
    submission_limit = 50
    supported_exts = [ "jpg", "png", "gif" ]

    def __init__(self, redis_conn, output_dir):
        self.redis_conn = redis_conn
        self.output_dir = os.path.abspath(output_dir)

        self.reddit = praw.Reddit(user_agent=self.agent)

    def _clean_title(self, title):
        return re.sub(r'([^\s\w]|_)+', '', title)[:128].lower()

    def _get_ext(self, url):
        url_info = urlparse.urlparse(url)
        return url_info.path.split(".")[-1].lower()

    def _seen(self, sub_id, subreddit):
        """ Check if we already have this submission. """
        return self.redis_conn.sismember(
            "stat:%s:processed:all" % subreddit, sub_id
        )

    def _save(self, sub_id, url, subreddit, filename, ext):
        """ Save submission and mark it as processed. """

        log.debug("Processing %s" % sub_id)

        subdir = self.output_dir + "/" + subreddit
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        suffix = 2
        full_file = "%s/%s.%s" % (subdir, filename, ext)
        while os.path.exists(full_file):
            full_file = "%s/%s_%s.%s" % (subdir, filename, suffix, ext)
            suffix += 1

        r = requests.get(url)
        with open(full_file, "wb") as output:
            output.write(r.content)

        # Increment saved number.
        self.redis_conn.incr("stat:%s:saved:count" % subreddit)
        # Add the download size to the total size.
        try:
            self.redis_conn.incrby(
                "stat:%s:saved:size" % subreddit,
                r.headers["content-length"]
            )
        except (AttributeError, KeyError, ResponseError):
            log.debug("Content-length is wrong: %s" % r.headers)
        # Add the donwload time.
        datehour = time.strftime("%Y%m%d%H", time.localtime())
        if not self.redis_conn.sismember(
                    "stat:%s:dates" % subreddit, datehour
                ):
            self.redis_conn.sadd(
                "stat:%s:dates" % subreddit, datehour
            )
        self.redis_conn.incr("stat:%s:date:%s" % (subreddit, datehour))

        log.info("Saved %s in %s: %s" % (sub_id, subreddit, filename))
        time.sleep(1)

    def process(self, sub):
        log.debug("Processing %s" % sub["name"])

        if not self.redis_conn.sismember("subreddits", sub["name"]):
            self.redis_conn.sadd("subreddits", sub["name"])

        if sub["type"] == "hot":
            submissions = self.reddit.get_subreddit(sub["name"]).get_hot(
                limit=self.submission_limit
            )
        elif sub["type"] == "new":
            submissions = self.reddit.get_subreddit(sub["name"]).get_new(
                limit=self.submission_limit
            )
        else:
            raise Exception("Unsupported type %s" % sub["type"])

        for submission in submissions:
            if self._seen(submission.id, sub["name"]):
                continue

            self.redis_conn.sadd(
                "stat:%s:processed:all" % sub["name"], submission.id
            )

            ext = self._get_ext(submission.url)
            if ext not in self.supported_exts:
                log.debug("Skipped %s, not supported extension in: %s" % (
                    submission.id, submission.url
                ))
                continue

            self._save(
                sub_id=submission.id,
                url=submission.url,
                subreddit=sub["name"],
                filename=self._clean_title(submission.title),
                ext=ext,
            )

        time.sleep(self.timeout)
