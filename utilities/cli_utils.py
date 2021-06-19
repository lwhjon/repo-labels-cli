"""
This module contains the command line interface (cli) utility methods
"""

import webbrowser

from utilities.extractor_facade import ExtractorFacade


def open_link(args):
    webbrowser.open(args.url, new=2)


def remove_trailing_slash_to_url(url):
    """
    Returns the input url without any trailing / if it had a trailing slash. This is useful for repository url
    where https://github.com/JonathanLeeWH/myrepo/ and https://github.com/JonathanLeeWH/myrepo both are equivalent
    hence for consistency we remove the trailing / for repository url
    :param url: The url to be formatted
    :return: Returns the url without any trailing /
    """

    return url[:-1] if url[-1] == '/' else url


def run_extractor(export_repo_link):
    response = ExtractorFacade().execute(export_repo_link)
    return response
