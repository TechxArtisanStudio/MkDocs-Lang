# MkDocs Multi-Language Project Manager

This tool helps manage multi-language MkDocs projects, allowing you to create, configure, clone, and manage multiple MkDocs sites within a single project structure.

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

## Installation

To install this tool, you need to clone the repository and use `pip` to install it locally. Follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:TechxArtisanStudio/MkDocs-Lang.git
   cd MkDocs-Lang
   ```

2. Install the package using `pip`:
   ```bash
   pip install .
   ```

This will make the `mklang` command available for system-wide CLI usage.

## Usage

The tool provides several command-line actions to manage your MkDocs projects:

### Create a New Project

Initialize a new MkDocs multi-language project directory.

```bash
mklang newproject --project /path/to/new/project/website-project --github <github-account>
# or using short options
mklang newproject -p /path/to/new/project/website-project -g <github-account>
```

### Create a New MkDocs Site

Add a new MkDocs site to your multi-language setup.

```bash
mklang new <mkdocs-site> --project <path-to-the-mainproject> --lang <language-code>
# or using short options
mklang new <mkdocs-site> -p <path-to-the-mainproject> -l <language-code>
```

### Clone GitHub Repositories

Clone an existing GitHub repository into your MkDocs project setup.

```bash
mklang addsite <repo-url> --lang <language-code> --project <path-to-main-project>
# or using short options
mklang addsite <repo-url> -l <language-code> -p <path-to-main-project>
```

### Execute a Custom Command

Run a custom command across all MkDocs sites within a specified directory structure.

```bash
mklang run "<the-customized-command-line>" --project /path/to/website-project
# or using short options
mklang run "<the-customized-command-line>" -p /path/to/website-project
```

### Remove a MkDocs Site

Remove a MkDocs site from the main project.

```bash
mklang removesite <site-name> --project <path-to-main-project>
# or using short options
mklang removesite <site-name> -p <path-to-main-project>
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 