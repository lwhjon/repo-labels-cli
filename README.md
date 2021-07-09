# 💻 RepoLabels command line interface

[![Application CI](https://github.com/lwhjon/repo-labels-cli/actions/workflows/app-test.yml/badge.svg)](https://github.com/lwhjon/repo-labels-cli/actions/workflows/app-test.yml)
[![CodeQL](https://github.com/lwhjon/repo-labels-cli/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/lwhjon/repo-labels-cli/actions/workflows/codeql-analysis.yml)
[![Python Version Requirement](https://img.shields.io/badge/Python-%3E=_3.9.5-blue)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/lwhjon/repo-labels-cli/blob/master/LICENSE)
[![Latest Stable Version)](https://img.shields.io/github/v/release/lwhjon/repo-labels-cli?color=blue&label=Latest%20Stable%20Version)](https://github.com/lwhjon/repo-labels-cli/releases/latest)
[![Latest Version including pre-releases)](https://img.shields.io/github/v/release/lwhjon/repo-labels-cli?color=blue&include_prereleases&label=Latest%20Version%20%28including%20pre%20releases%29)](https://github.com/lwhjon/repo-labels-cli/releases)

## 🎉 Introduction

**RepoLabels** is a GitHub Repository Labels command line interface which allows for easy exporting and importing of GitHub Labels.

## ✔ Purpose

The purpose of this project includes:

- Creating a tool which helps automate synchronisation of GitHub Labels for my personal usage and [use cases](#what-are-the-use-cases-of-repolabels).
- Serving as a practice for me to learn Python
- The usage of public APIs such as [GitHub API](https://docs.github.com/en/rest)

## 💡 What are the use cases of RepoLabels?

You can use **RepoLabels** to:

- Backup your GitHub labels.
- Import your GitHub labels to a different GitHub Repository.

### ✨ Benefits

- This avoids users having to manually reconfigure their labels when creating a new GitHub Repository or when planning to synchronise the labels of an existing repository which helps to save development time.

## 📌 Getting Started

A brief description on how to get your copy of **RepoLabels** running.

### 🛠 Requirements

We recommend using Python `3.9.5` (or later)

**Python packages dependencies**

Please refer to the [`requirements.txt`](https://github.com/lwhjon/repo-labels-cli/blob/master/requirements.txt) for the updated Python packages dependencies.

### 💾 Installation

1. Clone the **RepoLabels**'s GitHub Repository.
2. Create a `.env` file in the project root directory with the structure as shown below.

Sample `.env` file ([.env.sample](https://github.com/lwhjon/repo-labels-cli/blob/master/.env.example))

```Shell
# GitHub credentials
# Please refer to our documentation or GitHub documentation on how to retrieve your GitHub Personal Access Token.
# Resources:
# https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
GITHUB_USERNAME=YOUR_GITHUB_USERNAME
GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
```

**Note:** Please ensure that you key in all your desired values for the respective fields in the `.env` file.

3. Open your favourite terminal/command prompt in the **RepoLabels**'s working directory.
4. Create a virtual environment in Python in the directory of where **RepoLabels** is located.
   - `python -m venv <name_of_virtual_env>`
5. Activate the newly created virtual environment.
   - `<name_of_virtual_env>\Scripts\activate.bat` **(Windows)**
   - `<name_of_virtual_env>/bin/activate` **(Linux/Mac)**
6. Install the necessary Python package dependencies using the [`requirements.txt`](https://github.com/lwhjon/repo-labels-cli/blob/master/requirements.txt) included by **RepoLabels**
   - `pip install -r requirements.txt`
7. You can now use **RepoLabels**.
   - To view the list of available commands: `python repolabels.py --help`
8. A sample list of subcommands:

   - The `sync` subcommand can be used to `sync` labels from a GitHub Repository to another GitHub Repository

     - In the example below, we attempt to sync the labels from [https://github.com/github/docs](https://github.com/github/docs)'s GitHub Repository to a sample GitHub Repository:

       ```Shell
       python repolabels.py sync https://github.com/github/docs https://github.com/JonathanLeeWH/Sample
       ```

   - The `export` subcommand can be used to `export` labels from a GitHub Repository to a `json` format compatible with **RepoLabels**

     - In the example below, we attempt to `export` the labels from [https://github.com/github/docs](https://github.com/github/docs)'s GitHub Repository:

       ```Shell
       python repolabels.py export https://github.com/github/docs
       ```

       **Note:** By default, the `json` file will be exported to `exported/{repo_owner}_{repo_name}_{current date and time}.json`

       In the example above, the `json` file exported is located in `exported/github_docs_2021_06_27_19_20_50_283179.json`

       You can **change the export destination file path** using the `-d` flag followed by your desired destination file path.

   - The `import` subcommand can be used to `import` labels from a `json` format compatible with **RepoLabels** to a sample GitHub Repository.

     - In the example below, we attempt to `import` the labels from the `json` file we obtained from the `export` subcommand example above to a sample repository:

       ```Shell
       python repolabels.py import exported/github_docs_2021_06_27_19_20_50_283179.json https://github.com/JonathanLeeWH/Sample
       ```

   - The `rate-limit` subcommand can be used to check the current rate limits for each services such as GitHub API rate limits.

     ```Shell
      python repolabels.py rate-limit
     ```

   - The `update-cli` subcommand can be used to check the **Latest Stable Version** of **RepoLabels**.

     ```Shell
      python repolabels.py update-cli
     ```

_If you want to deactivate your current virtual environment, type `deactivate` in your command line or terminal._

## 🧰 Technologies and Frameworks

A list of the technologies and frameworks used in this project

### 🔎 APIs

- [GitHub API](https://docs.github.com/en/rest)

### ⚙ Others

- GitHub Actions for Continuous Integration (CI)
