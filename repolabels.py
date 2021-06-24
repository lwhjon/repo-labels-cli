"""
This module contains the main command line interface.
"""

import argparse
import json
import re
import sys
import logging

from pathlib import Path
from utilities.cli_utils import open_link, run_extractor, format_url, run_importer
from datetime import datetime

SOFTWARE_NAME = "Repository Labels command line interface"
VERSION = '1.0.0'
MAIN_PROJECT_REPO_LINK = "https://github.com/lwhjon/repo-labels-cli"
MAIN_EXPORT_DIRECTORY = Path.cwd().joinpath('exported')
# The default file name will be renamed to the format {repo_owner}_{repo_name}_{current date and time}.json
# if the default: exported/exported.json is used.
DEFAULT_EXPORT_FILE_NAME = 'exported.json'

debug_mode = False

# noinspection PyArgumentList
# Known Pycharm issue: https://youtrack.jetbrains.com/issue/PY-39762
logging.basicConfig(level=logging.DEBUG if debug_mode else logging.INFO,
                    format="%(asctime)s %(name)s %(funcName)s [%(levelname)s] %(message)s"
                    if debug_mode else "%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler('repolabels.log', mode='w'), logging.StreamHandler(sys.stdout)])
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
                                    "(default destination file path: "
                                    "'exported/{repo_owner}_{repo_name}_{current date and time}.json')")

    # Parser for "import" subcommand
    parser_import = subparsers.add_parser('import',
                                          help="Import labels from a compatible json file constructed from "
                                               "the 'export' subcommand to the repository.")
    parser_import.add_argument('import_cmd_repo_link',
                               help="Link to the repository in which the labels are to be imported to.")
    parser_import.add_argument('src_json_file_path', type=Path,
                               help="The source json file path in which the labels will be imported from.")

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
        current_export_url = format_url(args.export_cmd_repo_link)

        current_extractor = run_extractor(current_export_url)

        if current_extractor:
            file_path = args.dest_file_path.with_suffix('.json')
            repo_owner = current_extractor.repo_owner
            repo_name = current_extractor.repo_name
            # If the default directory file path is used,
            # rename the file_path to the format: 'exported/{repo_owner}_{repo_name}_{current date and time}.json'
            if args.dest_file_path == MAIN_EXPORT_DIRECTORY.joinpath(DEFAULT_EXPORT_FILE_NAME):
                file_path = MAIN_EXPORT_DIRECTORY.joinpath(
                    f"{repo_owner}_{repo_name}_{re.sub(r'[-.: ]', '_', str(datetime.now()))}.json")

            custom_json_list_labels = current_extractor.execute()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # To export the json file and prettify it.
            with open(file_path, mode='w') as json_file:
                json.dump(custom_json_list_labels, json_file, indent=4)
            logger.info(f'Labels from {args.export_cmd_repo_link} exported to {file_path}')

    # The logic for "import" subcommand with source json file path
    if hasattr(args, 'import_cmd_repo_link') and hasattr(args, 'src_json_file_path'):
        current_import_url = format_url(args.import_cmd_repo_link)

        current_importer = run_importer(current_import_url, src_json_file_path=args.src_json_file_path)

        if current_importer:
            current_importer.execute()
            logger.info(
                f'Labels from {args.src_json_file_path} has been successfully imported to {args.import_cmd_repo_link}')

    logger.info("Script execution completed")


if __name__ == "__main__":
    main()
