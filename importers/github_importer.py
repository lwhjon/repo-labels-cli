"""
This module contains the importer for GitHub.
GitHub: https://github.com/
"""

import logging

from importers.base_importer import BaseImporter
from pathlib import Path

logger = logging.getLogger(__name__)


class GitHubImporter(BaseImporter):

    def __init__(self, link, src_json_file_path: Path = None):
        super().__init__(link, src_json_file_path)

    def import_labels(self):
        pass

    def execute(self):
        if self.src_json_file_path:
            # Import the labels from a source json file path
            pass
        else:
            # TODO: Import the labels from a source repository url
            raise NotImplementedError
