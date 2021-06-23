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
            current_repo_link = repo_link
            parsed_url = urlparse(current_repo_link)
            hostname = parsed_url.hostname

            if hostname and hostname in ['www.github.com', 'github.com']:
                return GitHubExtractor(current_repo_link)
            else:
                raise SiteNotSupported(hostname)
        except SiteNotSupported as error:
            logger.error(error.message)
        return None
