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
from datetime import datetime
from extractors.base_extractor import BaseExtractor
from utilities.config import GITHUB_USERNAME, GITHUB_PERSONAL_ACCESS_TOKEN
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class GitHubExtractor(BaseExtractor):

    def __init__(self, link):
        super().__init__(link)
        self.main_api_link = 'https://api.github.com'
        self.accept_header = 'application/vnd.github.v3+json'
        # Max number of labels per page allowed by GitHub API for retrieval of the list of labels in repository is 100
        # https://docs.github.com/en/rest/reference/issues#list-labels-for-a-repository
        self.per_page = 100
        self.total_num_pages_labels = None
        self.repo_owner, self.repo_name = self.parse_github_link(link)
        self.labels_api_link = f'{self.main_api_link}/repos/{self.repo_owner}/{self.repo_name}/labels'
        self.authentication = BasicAuth(GITHUB_USERNAME, password=GITHUB_PERSONAL_ACCESS_TOKEN)

    @staticmethod
    def parse_github_link(link):
        parsed_url_path = urlparse(link).path.split('/')
        if len(parsed_url_path) >= 3:
            repo_owner = parsed_url_path[1]
            repo_name = parsed_url_path[2]
            return repo_owner, repo_name
        return None, None

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

    async def get_rate_limit(self):
        """
        Returns Service name, the total rate limit, remaining rate limit, rate limit used and time which rate limit will reset.
        Note: This function returns the rate limit for GitHub API Resources core component
        as the GitHub API requests used by RepoLabels are in the core component GitHub API Resources.
        :return: Returns the total rate limit, remaining rate limit, rate limit used and time
        which rate limit will reset.
        """
        api_headers = {'Accept': self.accept_header}
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.main_api_link}/rate_limit', params=api_headers,
                                   auth=self.authentication) as response:
                result = await response.json()
                result = result['resources']['core']
                return "GitHub API", result['limit'], result['remaining'], result['used'], \
                       datetime.fromtimestamp(result['reset'])

    async def get_num_of_pages(self, session):
        """
        TODO: Possibly removed in the future including beautifulsoup dependencies as the function is currently not used.
        Alternative method to retrieve the number of pages based on the response retrieved from GitHub API
        Benefit: It does not use API calls hence, would not be counted in the GitHub API rate limit.
        Note: However, it currently only works for public repository.
        :param session: The session object
        :return: Returns the number of pages based on the response retrieved from GitHub API
        """
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
            # Optimisation: If it is the first page, besides retrieving the json response,
            # the total number of pages is also retrieved in a single API call. This is to reduce unnecessary API calls.
            if request_params['page'] == 1:
                query_string = urlparse(str(response.links.get('last').get('url'))).query if \
                    response.links.get('last') else None
                self.total_num_pages_labels = \
                    int(parse_qs(query_string)['page'][0]) if query_string else 1
            logger.debug(f'get_labels method page request information {response.request_info}')
            current_labels = await response.json()
            logger.debug(f'labels list json from GitHub API: {json.dumps(current_labels)}')
            return self.gen_custom_labels_dict(current_labels)

    async def request_labels(self):
        api_headers = {'Accept': self.accept_header}
        async with aiohttp.ClientSession(headers=api_headers, auth=self.authentication) as session:
            tasks = []
            custom_labels_dict_json = dict()

            is_first = True
            num_of_pages = 1
            current_page_num = 1
            while current_page_num <= num_of_pages:
                params = {'per_page': self.per_page, 'page': current_page_num}

                if is_first:
                    response = await self.get_labels_dict(session, params)
                    custom_labels_dict_json.update(response)
                    logger.debug(custom_labels_dict_json)
                    num_of_pages = self.total_num_pages_labels
                    is_first = False
                else:
                    tasks.append(asyncio.ensure_future(self.get_labels_dict(session, params)))

                current_page_num += 1

            if tasks:
                custom_json_list_labels = await asyncio.gather(*tasks)
                logger.debug(custom_json_list_labels)

                # To convert the list to a dictionary (custom format json compatible with
                # this command line interface)
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
