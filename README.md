# RepoLabels command line interface
**RepoLabels** is a GitHub Repository Labels command line interface which allows for easy exporting and importing of GitHub Labels.

# What are the use cases of RepoLabels?
You can use **RepoLabels** to:
- Backup your GitHub labels
- Import your GitHub labels to a different GitHub Repository.

## Benefits
- This avoids users having to manually reconfigure your labels when creating a new GitHub Repository or when planning to synchronise the labels of an existing repository. 

# Getting Started
A brief description on how to get your copy of **RepoLabels** running.

## Requirements
We recommend using Python `3.9.5` (or the latest Python version)

**Python packages dependencies**

Please refer to the [`requirements.txt`](https://github.com/lwhjon/repo-labels-cli/blob/master/requirements.txt) for the updated Python packages dependencies.

## Installation
1. Open your command line or terminal and go to the directory where you installed **RepoLabelsp**.
2. Create a virtual environment in Python in the directory of where **RepoLabels** is located.
   *  `python -m venv <name_of_virtual_env>`
3. Activate the newly created virtual environment.
   * `<name_of_virtual_env>\Scripts\activate.bat` **(Windows)**
   * `<name_of_virtual_env>/bin/activate` **(Linux/Mac)**
4. Install the necessary Python package dependencies using the requirements.txt included by **RepoLabels**
   * `pip install -r requirements.txt` 
5. You can now use **RepoLabels**.
   * `python repolabels.py`

*If you want to deactivate your current virtual environment, you can just type `deactivate` in your command line or terminal.*

# Purpose
The purpose of this project includes:
- Creating a tool which helps automate synchronisation of GitHub Labels for my personal usage and [use cases](#what-are-the-use-cases-of-repolabels).
- Serving as a practice for me to learn Python
- The usage of public APIs such as [GitHub API](https://docs.github.com/en/rest)
