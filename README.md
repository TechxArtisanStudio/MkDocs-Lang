# mkdocs-lang

`mkdocs-lang` is a Python-based CLI tool designed to simplify the management of multi-language MkDocs projects. It automates the creation of projects containing multiple language-specific MkDocs sites, file synchronization, deletion, Git operations, and configuration.

## Overview

Managing **multi-language MkDocs projects** can be tedious, especially when each language version is a **separate MkDocs site** but follows the **same structure**. This tool aims to streamline the process by organizing these sites within a single directory structure, providing better maintainability, flexibility, and ease of installation.

### Project Structure

We recommend organizing your MkDocs sites in different languages with the following structure:

```
/website-project/      # Main Project Directory
├── mkdocs-lang.yml
├── mkdocs.yml.template
├── requirements.txt
├── venv/
├── mk-website_en/     # MkDocs site in English
│   ├──docs/
│   ├──mkdocs.yml
├── mk-website_fr/     # MkDocs site in French
├── mk-website_de/     # MkDocs site in German
...
```

This structure allows for centralized management of all language-specific MkDocs sites, making it easier to synchronize files, manage configurations, and perform Git operations.

## Features

- **File and directory synchronization** across multiple MkDocs sites.
- **Automated Git actions** like clone, status, pull, and sync (commit & push).
- **Configurable list of MkDocs sites** that allows each site to be stored in any path.
- **Universal command execution** across all MkDocs sites.
- **Installation as a Python package** (`pip install mkdocs-lang`) for system-wide CLI usage.

## Installation

To install `mkdocs-lang`, clone the repository and install the package using pip:

```bash
git clone https://github.com/your-github/mkdocs-lang.git
cd mkdocs-lang
pip install .
```

## Key Actions

- **`newproject`**: Creates a new project folder with a `mkdocs-lang.yml` file. [Learn more](docs/1-create-a-new-project.md)
- **`new`**: Creates a new MkDocs site. [Learn more](docs/2-create-a-brand-new-mkdocs-project.md)
- **`gitclone`**: Clones a GitHub repository into the main project and updates configuration. [Learn more](docs/3-add-github-repos.md)
- **`cl`**: Executes a custom command across all MkDocs sites. [Learn more](docs/4-add-universal-action.md)
- **`config`**: Manages the list of MkDocs sites and updates GitHub account.
- **`copy`**: Copies files across all MkDocs sites.
- **`del`**: Deletes a file or directory across sites.
- **`git`**: Runs Git actions across all sites.

## Quick Start

Here are some basic command lines to get you started with `mkdocs-lang`:

- **Create a New Project**

  ```bash
  mklang newproject --project /path/to/new/project/website-project --github <github-account>
  ```

- **Add a New MkDocs Site**

  ```bash
  mklang new <mkdocs-site> --project <path-to-the-mainproject> --lang <language-code>
  ```

- **Clone a GitHub Repository**

  ```bash
  mklang gitclone <repo-url> --lang <language-code> --project <path-to-main-project>
  ```

- **Execute a Custom Command Across All Sites**

  ```bash
  mklang cl "<the-customized-command-line>" --project /path/to/website-project
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 