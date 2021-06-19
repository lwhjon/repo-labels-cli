"""
This module contains the exceptions that are used by extractors.
"""


class SiteNotSupported(Exception):
    def __init__(self, hostname):
        self.message = f"SiteNotSupported: {hostname} Repository host not supported."
