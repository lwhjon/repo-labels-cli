"""
This module contains the command line interface (cli) utility methods
"""

import webbrowser
from pathlib import Path
from urllib.parse import urlparse
from utilities.extractor_facade import ExtractorFacade
from utilities.importer_facade import ImporterFacade


def open_link(args):
    webbrowser.open(args.url, new=2)


def remove_trailing_slash_to_url(url):
    """
    Returns the input url without any trailing / if it had a trailing slash. This is useful for repository url
    where https://github.com/lwhjon/repo-labels-cli/ and https://github.com/lwhjon/repo-labels-cli both are equivalent
    hence for consistency we remove the trailing / for repository url
    :param url: The url to be formatted
    :return: Returns the url without any trailing /
    """

    return url[:-1] if url[-1] == '/' else url


def format_url(url):
    """
    Returns the formatted url such as removing trailing slash as well as prepending https:// to the url
    if the url does not have a scheme
    :param url: The url to be formatted
    :return: Returns the formatted url
    """

    current_url = remove_trailing_slash_to_url(url)
    parsed_url = urlparse(current_url)

    # To consider the case where the url does not have a scheme such as github.com without https prepended
    if not parsed_url.scheme:
        current_url = f'https://{current_url}'
        parsed_url = urlparse(current_url)

    return parsed_url.geturl()


def run_extractor(export_repo_link):
    response = ExtractorFacade().execute(export_repo_link)
    return response


def run_importer(import_repo_link, src_json_file_path: Path = None):
    response = ImporterFacade().execute(import_repo_link, src_json_file_path)
    return response
