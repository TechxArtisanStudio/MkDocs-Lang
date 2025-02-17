### 1. Create a New Project

The `newproject` action initializes a new MkDocs multi-language project directory.

#### Usage

```bash
mklang newproject --project /path/to/new/project/website-project --github <github-account>
# or using short options
mklang newproject -p /path/to/new/project/website-project -g <github-account>
```

- `--github` (`-g`) is optional. If specified, it writes the GitHub account into `mkdocs-lang.yml`. Otherwise, it defaults to 'your-github-account'.
- You can update the GitHub account information for `mkdocs-lang.yml` later by using the `config` action.

#### What It Does

1. Creates a new project directory named `website-project`.
2. Sets up a Python virtual environment for shared use across all language-specific MkDocs sites.
3. Generates `mkdocs-lang.yml` with the absolute path of the main project and a `mkdocs.yml.template`.
4. Creates `requirements.txt` with `mkdocs-material`.
5. Installs the packages listed in `requirements.txt` into the virtual environment.

#### Project Structure

After running the command, your project directory will look like this:

```
/website-project/
├── mkdocs-lang.yml
├── mkdocs.yml.template
├── requirements.txt
├── venv/
```

#### Definitions

- **Project**: The main directory where all MkDocs sites for different languages are stored.
- **Site**: An individual MkDocs site for a specific language within the project. 