""" Parsing utilities.
"""

def setup_parser(parser, commands):
    subparsers = parser.add_subparsers()

    for name, command in commands.iteritems():
        sub_parser = subparsers.add_parser(name, help=command.help)
        command.setup_parser(sub_parser)
        sub_parser.set_defaults(
            command=command
        )
