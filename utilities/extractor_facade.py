"""
This module contains the ExtractorFacade which calls the appropriate method from the appropriate classes
based on the parameter passed.
"""

import logging

from urllib.parse import urlparse
from exceptions.extractor_exceptions import SiteNotSupported
from extractors.github_extractor import GitHubExtractor

logger = logging.getLogger(__name__)


class ExtractorFacade:

    @staticmethod
    def execute(repo_link: str):
        try:
            parsed_url = urlparse(repo_link)
            hostname = parsed_url.netloc

            # To consider the case where the url does not have a scheme such as github.com without https prepended
            if not parsed_url.scheme:
                parsed_url = urlparse(f'https://{repo_link}')
                hostname = parsed_url.netloc

            if "github.com" in hostname:
                GitHubExtractor(repo_link).execute()
            else:
                raise SiteNotSupported(hostname)
        except SiteNotSupported as error:
            logger.error(error.message)
