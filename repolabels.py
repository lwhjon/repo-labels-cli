"""
This module contains the main command line interface.
"""

import argparse
import sys
import logging

from utilities.cli_utils import open_link, run_extractor, remove_trailing_slash_to_url

SOFTWARE_NAME = "Repository Labels command line interface"
VERSION = '1.0.0'
MAIN_PROJECT_REPO_LINK = "https://github.com/JonathanLeeWH/repo-labels-cli"

logging.basicConfig(filename='repolabels.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=f'{SOFTWARE_NAME} is a command line interface to manage GitHub Repository labels.')

    subparsers = parser.add_subparsers(description="A list of possible subcommands")

    # Parser for "export" subcommand
    parser_export = subparsers.add_parser('export',
                                          help="Exports labels from the repository in a compatible format "
                                               "as a json file.")
    parser_export.add_argument('export_repo_link', help="Link to the repository in which the labels are exported from.")

    # Parser for "website" subcommand
    parser_website = subparsers.add_parser('website', help=f'Redirects to the {SOFTWARE_NAME} project website')
    parser_website.set_defaults(func=open_link,
                                url=MAIN_PROJECT_REPO_LINK)

    args = parser.parse_args()

    logger.info("Start executing script")

    if hasattr(args, 'func'):
        args.func(args)

    if len(sys.argv) == 1:
        parser.print_help()

    if hasattr(args, 'export_repo_link'):
        run_extractor(remove_trailing_slash_to_url(args.export_repo_link))

    logger.info("Script execution completed")


if __name__ == "__main__":
    main()
