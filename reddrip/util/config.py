import ConfigParser


class Configuration(object):
    def __init__(self, config_file):
        """ Configuration object.

        This object holds all runtime configuration read from the file.

        :param config_file: Configuration file path.
        :type config_file: string
        """
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        self.glob = {}
        self.subs = {}

        for section in config.sections():
            for item in config.items(section):
                name, value = item
                if section == "global":
                    self.glob[name] = value
                elif section.startswith("subreddit"):
                    _, subreddit = section.split(":")
                    if not self.subs.get(subreddit, False):
                        self.subs[subreddit] = {}
                        self.subs[subreddit]["name"] = subreddit

                    self.subs[subreddit][name] = value

    def __len__(self):
        return len(self.subs)

    def subreddits(self):
        for subreddit in self.subs.itervalues():
            yield subreddit

    def subreddit(self, name):
        return self.subs[name]
