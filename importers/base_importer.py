"""
This module contains the BaseImporter Abstract class which all other importers are inherited from.
"""
from abc import ABC, abstractmethod
from pathlib import Path


class BaseImporter(ABC):

    def __init__(self, link, src_json_file_path: Path = None):
        self.link = link
        self.src_json_file_path = src_json_file_path
        self.repo_owner = None
        self.repo_name = None

    @abstractmethod
    def import_labels(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError
