"""
This module contains the exceptions that are commonly used.
"""


class SiteNotSupported(Exception):
    def __init__(self, hostname):
        self.message = f"SiteNotSupported: {hostname} Repository host not supported."
