import argparse

from reddrip.util.log import setup_logging
from reddrip.util.parse import setup_parser
# Import commands.
from reddrip.commands.run import RunCommand
from reddrip.commands.stat import StatCommand

def main(args):
    """ Main entry point for the CLI scripts."""

    early_parser = argparse.ArgumentParser(
        # Turn off help, so that we can show all options in the real parser.
        add_help=False,
    )
    early_parser.add_argument(
        "--verbose", "-v", default=False, action="store_true",
        help="verbose logging"
    )

    # Bootstrap the context.
    (options, additional_args) = early_parser.parse_known_args(args)
    setup_logging(verbose=options.verbose, color=True)

    # Now initialize the real parser.
    parser = argparse.ArgumentParser(
        parents=[ early_parser ],
        description="Command line interface for Reddrip.",
    )

    commands = {
        "run": RunCommand,
        "stat": StatCommand,
    }
    setup_parser(parser, commands)

    # Parse the rest of the command arguments.
    options = parser.parse_args(args)

    command = options.command()
    command.execute(options)
