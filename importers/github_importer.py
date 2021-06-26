"""
This module contains the importer for GitHub.
GitHub: https://github.com/
"""

import asyncio
import logging
import os
import aiohttp

from aiohttp import BasicAuth
from extractors.github_extractor import GitHubExtractor
from importers.base_importer import BaseImporter
from utilities.config import GITHUB_USERNAME, GITHUB_PERSONAL_ACCESS_TOKEN

logger = logging.getLogger(__name__)


class GitHubImporter(BaseImporter):

    def __init__(self, link, loaded_json_data):
        super().__init__(link, loaded_json_data)
        self.main_api_link = 'https://api.github.com'
        self.accept_header = 'application/vnd.github.v3+json'
        self.repo_owner, self.repo_name = GitHubExtractor.parse_github_link(link)
        self.labels_api_link = f'{self.main_api_link}/repos/{self.repo_owner}/{self.repo_name}/labels'
        self.existing_labels_json = None
        self.labels_encountered = set()
        self.authentication = BasicAuth(GITHUB_USERNAME, password=GITHUB_PERSONAL_ACCESS_TOKEN)

    async def create_label(self, session, properties):
        async with session.post(self.labels_api_link, json=properties) as response:
            logger.debug(response.request_info)
            result = await response.json()
            logger.debug(result)
            return result

    async def update_label(self, session, label_name, new_properties):
        async with session.patch(f'{self.labels_api_link}/{label_name}', json=new_properties) as response:
            logger.debug(response.request_info)
            result = await response.json()
            logger.debug(result)
            return result

    async def delete_label(self, session, label_name):
        async with session.delete(f'{self.labels_api_link}/{label_name}') as response:
            logger.debug(response.request_info)
            return True

    async def import_labels(self):
        api_headers = {'Accept': self.accept_header}
        async with aiohttp.ClientSession(headers=api_headers, auth=self.authentication) as session:
            tasks = []
            for current_label_name in self.json_data.keys():
                self.labels_encountered.add(current_label_name)
                if current_label_name in self.existing_labels_json.keys():
                    # Optimisation: If the label and its properties in the repository are identical to the json file,
                    # there will not be any API calls. This is to reduce unnecessary API calls.
                    if self.json_data[current_label_name] == self.existing_labels_json[current_label_name]:
                        continue
                    else:
                        json_properties = self.json_data[current_label_name]
                        new_properties = {
                            **json_properties
                        }
                        new_properties['new_name'] = new_properties['name']
                        del new_properties['name']
                        tasks.append(asyncio.ensure_future(
                            self.update_label(session, self.existing_labels_json[current_label_name]['name'],
                                              new_properties)))
                else:
                    tasks.append(asyncio.ensure_future(self.create_label(session, self.json_data[current_label_name])))

            labels_not_in_json = set(self.existing_labels_json.keys()).difference(self.labels_encountered)
            for current_label_name in labels_not_in_json:
                tasks.append(asyncio.ensure_future(
                    self.delete_label(session, self.existing_labels_json[current_label_name]['name'])))

            if tasks:
                await asyncio.gather(*tasks)

    def execute(self):
        """
        This is the main function which will be executed to run the GitHub importer.
        :return: It returns True if import is successful and false if it is not successful.
        """

        extractor = GitHubExtractor(self.link)
        self.existing_labels_json = extractor.execute()
        logger.debug(self.existing_labels_json)

        # Workaround for known issue involving event loop for Windows environment:
        # Resources:
        # https://github.com/aio-libs/aiohttp/issues/4536#issuecomment-698441077
        # https://bugs.python.org/issue39232 (Known issue in Python)
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.import_labels())
