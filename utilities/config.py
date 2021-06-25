"""
This module handles environmental variables
"""

import os

from dotenv import load_dotenv

load_dotenv()

# GitHub credentials
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
