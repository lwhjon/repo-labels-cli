"""
This module contains the BaseImporter Abstract class which all other importers are inherited from.
"""
from abc import ABC, abstractmethod

from utilities.constants import ImportModes


class BaseImporter(ABC):

    def __init__(self, link, loaded_json_data):
        self.link = link
        self.json_data = loaded_json_data
        self.repo_owner = None
        self.repo_name = None

    @abstractmethod
    def import_labels(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, mode: ImportModes):
        raise NotImplementedError
