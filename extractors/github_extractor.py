"""
This module contains the extractor for GitHub.
GitHub: https://github.com/
"""

import json
import os
import aiohttp
import asyncio
import logging

from aiohttp import BasicAuth
from bs4 import BeautifulSoup
from extractors.base_extractor import BaseExtractor
from utilities.config import GITHUB_USERNAME, GITHUB_PERSONAL_ACCESS_TOKEN
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class GitHubExtractor(BaseExtractor):

    def __init__(self, link):
        super().__init__(link)
        self.main_api_link = 'https://api.github.com'
        self.accept_header = 'application/vnd.github.v3+json'
        # Max number of pages allowed by GitHub API for list of labels in repository is 100
        # https://docs.github.com/en/rest/reference/issues#list-labels-for-a-repository
        self.per_page = 100
        self.repo_owner, self.repo_name = self.parse_github_link(link)
        self.labels_api_link = f'{self.main_api_link}/repos/{self.repo_owner}/{self.repo_name}/labels'
        self.authentication = BasicAuth(GITHUB_USERNAME, password=GITHUB_PERSONAL_ACCESS_TOKEN)

    @staticmethod
    def parse_github_link(link):
        parsed_url_path = urlparse(link).path.split('/')
        repo_owner = parsed_url_path[1]
        repo_name = parsed_url_path[2]
        return repo_owner, repo_name

    @staticmethod
    def gen_custom_labels_dict(list_of_label_dict):
        custom_labels_dict = dict()
        for current_label_dict in list_of_label_dict:
            current_label_name = current_label_dict['name'].lower()
            custom_labels_dict[current_label_name] = {
                **current_label_dict
            }
            del custom_labels_dict[current_label_name]['id']
            del custom_labels_dict[current_label_name]['node_id']
            del custom_labels_dict[current_label_name]['url']
            del custom_labels_dict[current_label_name]['default']
        return custom_labels_dict

    async def get_num_of_pages(self, session):
        # TODO: Add support for private repository
        non_api_link_to_labels = f'{self.link}/labels'
        async with session.get(non_api_link_to_labels, headers={"Accept": "text/html"}) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            num_of_labels = int(soup.select('div.labels-list span.js-labels-count', limit=1)[0].contents[0])
            num_of_pages = (num_of_labels // self.per_page) + (1 if num_of_labels % self.per_page != 0 else 0)
            logger.debug(f'{self.link} has {num_of_pages} pages.')
            return num_of_pages

    async def get_labels_dict(self, session, request_params):
        """
        Returns a dictionary of labels with customised properties based on the list of labels retrieved from the
        GitHub API
        :param session: The session object
        :param request_params: The request_params which should contain the per_page and page params
        :return: Returns a dictionary of labels with customised properties.
        """
        async with session.get(self.labels_api_link, params=request_params) as response:
            logger.debug(f'get_labels method page request information {response.request_info}')
            current_labels = await response.json()
            logger.debug(f'labels list json from GitHub API: {json.dumps(current_labels)}')
            return self.gen_custom_labels_dict(current_labels)

    async def request_labels(self):
        api_headers = {'Accept': self.accept_header}
        async with aiohttp.ClientSession(headers=api_headers, auth=self.authentication) as session:
            num_of_pages = await self.get_num_of_pages(session)
            tasks = []
            for current_page_num in range(1, num_of_pages + 1):
                params = {'per_page': self.per_page, 'page': current_page_num}
                tasks.append(asyncio.ensure_future(self.get_labels_dict(session, params)))
            custom_json_list_labels = await asyncio.gather(*tasks)
            logger.debug(custom_json_list_labels)

            # To convert to the list to a dictionary (custom format json compatible with this command line interface)
            custom_labels_dict_json = dict()
            for current_dict in custom_json_list_labels:
                logger.debug(current_dict)
                custom_labels_dict_json.update(current_dict)

            logger.debug(custom_labels_dict_json)
            return custom_labels_dict_json

    def execute(self):
        """
        This is the main function which will be executed to run the GitHub extractor.
        It returns a dictionary of labels with customised properties compatible with this command line interface.
        :return: It returns a dictionary of labels with customised properties compatible
        with this command line interface
        """

        # Workaround for known issue involving event loop for Windows environment:
        # Resources:
        # https://github.com/aio-libs/aiohttp/issues/4536#issuecomment-698441077
        # https://bugs.python.org/issue39232 (Known issue in Python)
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        custom_labels_dict_json = asyncio.run(self.request_labels())
        logger.debug(custom_labels_dict_json)
        logger.debug(json.dumps(custom_labels_dict_json))
        logger.debug(len(custom_labels_dict_json.keys()))

        return custom_labels_dict_json
