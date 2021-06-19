"""
This module contains the extractor for GitHub.
GitHub: https://github.com/
"""

import json
import os
import aiohttp
import asyncio
import logging

from bs4 import BeautifulSoup
from extractors.base_extractor import BaseExtractor
from urllib.parse import urlparse
from itertools import chain

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
        self.labels_encountered = set()

    @staticmethod
    def parse_github_link(link):
        parsed_url_path = urlparse(link).path.split('/')
        repo_owner = parsed_url_path[1]
        repo_name = parsed_url_path[2]
        return repo_owner, repo_name

    def gen_custom_labels_list(self, list_of_label_dict):
        custom_labels_list = []
        for current_label_dict in list_of_label_dict:
            constructed_dict = {
                **current_label_dict
            }
            del constructed_dict['id']
            del constructed_dict['node_id']
            del constructed_dict['url']
            del constructed_dict['default']
            self.labels_encountered.add(constructed_dict['name'])
            custom_labels_list.append(constructed_dict)
        return custom_labels_list

    async def get_num_of_pages(self, session):
        non_api_link_to_labels = f'{self.link}/labels'
        async with session.get(non_api_link_to_labels, headers={"Accept": "text/html"}) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            num_of_labels = int(soup.select('div.labels-list span.js-labels-count', limit=1)[0].contents[0])
            num_of_pages = (num_of_labels // self.per_page) + (1 if num_of_labels % self.per_page != 0 else 0)
            logger.debug(f'{self.link} has {num_of_pages} pages.')
            return num_of_pages

    async def get_labels_list(self, session, request_params):
        """
        Returns the list of labels with customised properties based on the list of labels retrieved from the GitHub API
        :param session: The session object
        :param request_params: The request_params which should contain the per_page and page params
        :return: The list of labels with customised properties.
        """
        async with session.get(self.labels_api_link, params=request_params) as response:
            logger.debug(f'get_labels method page request information {response.request_info}')
            current_labels = await response.json()
            logger.debug(f'labels list json {json.dumps(current_labels)}')
            return self.gen_custom_labels_list(current_labels)

    async def request_labels(self):
        api_headers = {'Accept': self.accept_header}
        params = {'per_page': self.per_page}
        async with aiohttp.ClientSession(headers=api_headers) as session:
            num_of_pages = await self.get_num_of_pages(session)
            tasks = []
            for current_page_num in range(1, num_of_pages + 1):
                params['page'] = current_page_num
                tasks.append(asyncio.ensure_future(self.get_labels_list(session, params)))

            custom_json_list_labels = await asyncio.gather(*tasks)
            # To flatten the lists
            custom_json_list_labels = list(chain.from_iterable(custom_json_list_labels))
            logger.debug(custom_json_list_labels)
            return custom_json_list_labels

    def execute(self):
        # Workaround for known issue involving event loop for Windows environment:
        # Resources:
        # https://github.com/aio-libs/aiohttp/issues/4536#issuecomment-698441077
        # https://bugs.python.org/issue39232 (Known issue in Python)
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        custom_json_list_labels = asyncio.run(self.request_labels())

        logger.debug(json.dumps(custom_json_list_labels))
        logger.debug(len(custom_json_list_labels))

        # To export the json file and prettify it.
        with open('exported.json', mode='w') as json_file:
            json.dump(custom_json_list_labels, json_file, indent=4)
