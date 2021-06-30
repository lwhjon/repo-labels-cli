"""
This module contains the command line interface (cli) utility methods
"""

import asyncio
import logging
import os
import webbrowser

from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen
from utilities.extractor_facade import ExtractorFacade
from utilities.importer_facade import ImporterFacade

DEFAULT_SERVICES = ['https://github.com']

logger = logging.getLogger(__name__)


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


async def request_rate_limits(services):
    tasks = []
    for service in services:
        service_object = ExtractorFacade().execute(service)
        tasks.append(asyncio.ensure_future(service_object.get_rate_limit()))

    rate_limit_results = await asyncio.gather(*tasks)
    return rate_limit_results


def rate_limits(services=DEFAULT_SERVICES):
    # Workaround for known issue involving event loop for Windows environment:
    # Resources:
    # https://github.com/aio-libs/aiohttp/issues/4536#issuecomment-698441077
    # https://bugs.python.org/issue39232 (Known issue in Python)
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    results = asyncio.run(request_rate_limits(services))

    for current_result in results:
        service_name, total_rate_limit, rate_limit_remaining, rate_limit_used, rate_limit_reset_time = current_result
        header = f'{service_name} Rate Limits Information'
        response = f"\n\n{header}\n" \
                   f"{'=' * len(header)}\n" \
                   f"Total Rate Limit: {total_rate_limit}\n" \
                   f"Total Rate Limit Remaining: {rate_limit_remaining}\n" \
                   f"Total Rate Limit used: {rate_limit_used}\n" \
                   f"{service_name} API Rate Limit resets at {rate_limit_reset_time}\n"
        logger.info(f'Rate Limits Information: {response}')


def validate_url(url):
    """
    To check if the internet connection is present and that the input url is valid else an error will be outputted
    and the program exits with exit code 1.
    :param url: The input url to be validated.
    :return:
    """
    try:
        urlopen(format_url(url), timeout=8)
    except (URLError, ValueError):
        logger.error(f'Please ensure that {url} is a valid url and that you are connected to the internet.')
        raise SystemExit(1)
