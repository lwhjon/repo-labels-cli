"""
This module contains the ImporterFacade which calls the appropriate method from the appropriate classes
based on the parameter passed.
"""

import logging

from urllib.parse import urlparse
from exceptions.general_exceptions import SiteNotSupported
from importers.github_importer import GitHubImporter

logger = logging.getLogger(__name__)


class ImporterFacade:

    @staticmethod
    def execute(repo_link: str, loaded_json_data):
        try:
            current_repo_link = repo_link
            parsed_url = urlparse(current_repo_link)
            hostname = parsed_url.hostname

            if hostname and hostname in ['www.github.com', 'github.com']:
                return GitHubImporter(current_repo_link, loaded_json_data)
            else:
                raise SiteNotSupported(hostname)
        except SiteNotSupported as error:
            logger.error(error.message)
        return None
