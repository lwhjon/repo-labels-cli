"""
This module contains the main command line interface.
"""

import argparse
import json
import sys
import logging

from pathlib import Path
from utilities.cli_utils import open_link, run_extractor, remove_trailing_slash_to_url

SOFTWARE_NAME = "Repository Labels command line interface"
VERSION = '1.0.0'
MAIN_PROJECT_REPO_LINK = "https://github.com/JonathanLeeWH/repo-labels-cli"
MAIN_EXPORT_DIRECTORY = Path.cwd().joinpath('exported')
DEFAULT_EXPORT_FILE_NAME = 'exported.json'

logging.basicConfig(filename='repolabels.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=f'{SOFTWARE_NAME} is a command line interface to manage GitHub Repository labels.')
    parser.add_argument('--version', action='version', version=f'{SOFTWARE_NAME} Version {VERSION}')

    subparsers = parser.add_subparsers(description="A list of possible subcommands")

    # Parser for "export" subcommand
    parser_export = subparsers.add_parser('export',
                                          help="Exports labels from the repository in a compatible format "
                                               "as a json file.")
    parser_export.add_argument('export_cmd_repo_link',
                               help="Link to the repository in which the labels are exported from.")
    parser_export.add_argument('-d', '--dest_file_path',
                               default=MAIN_EXPORT_DIRECTORY.joinpath(DEFAULT_EXPORT_FILE_NAME),
                               type=Path,
                               help="The destination file path in which the exported labels will be exported to. "
                                    "(default destination file path: 'exported/exported.json')")

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

    # The logic for "export" subcommand
    if hasattr(args, 'export_cmd_repo_link'):
        file_path = args.dest_file_path.with_suffix('.json')
        custom_json_list_labels = run_extractor(remove_trailing_slash_to_url(args.export_cmd_repo_link))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # To export the json file and prettify it.
        with open(file_path, mode='w') as json_file:
            json.dump(custom_json_list_labels, json_file, indent=4)
        logger.info(f'Labels from {args.export_cmd_repo_link} exported to {file_path}')

    logger.info("Script execution completed")


if __name__ == "__main__":
    main()
