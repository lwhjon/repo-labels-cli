"""
This module contains the BaseExtractor Abstract class which all other extractors are inherited from.
"""
from abc import ABC, abstractmethod


class BaseExtractor(ABC):

    def __init__(self, link):
        self.link = link
        self.labels = set()
        self.repo_owner = None
        self.repo_name = None

    @abstractmethod
    def request_labels(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError
