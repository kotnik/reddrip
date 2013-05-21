""" Base command definition.
"""

class Command(object):
    help = ""

    def __init__(self):
        pass

    @classmethod
    def setup_parser(cls, parser):
        pass
