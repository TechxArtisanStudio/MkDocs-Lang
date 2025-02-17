## Create a New MkDocs Multi-Language Project

The `newproject` action initializes a new MkDocs multi-language project directory.

### Usage

```bash
mklang newproject --project /path/to/new/project/website-project --github <github-account>
# or using short options
mklang newproject -p /path/to/new/project/website-project -g <github-account>
```

### Options

- `--project`, `-p`: Specify the path to the new project directory.
- `--github`, `-g`: (Optional) Specify the GitHub account to be written into `mkdocs-lang.yml`. Defaults to 'your-github-account'.

### What It Does

1. **Creates a New Project Directory**: Initializes a directory named `website-project`.
2. **Sets Up a Python Virtual Environment**: Creates a virtual environment for shared use across all language-specific MkDocs sites.
3. **Generates Configuration Files**:
   - `mkdocs-lang.yml`: Contains the main project path and GitHub account information.
   - `mkdocs.yml.template`: A template for MkDocs configuration.
   - `requirements.txt`: Lists `mkdocs-material` as a dependency.
4. **Installs Requirements**: Installs the packages listed in `requirements.txt` into the virtual environment.
5. **Creates `repos.txt` Template**: Provides a template for batch cloning repositories.

### Project Structure

After running the command, your project directory will look like this:

```
/website-project/
├── mkdocs-lang.yml
├── mkdocs.yml.template
├── requirements.txt
├── repos.txt
├── venv/
```

### Definitions

- **Project**: The main directory where all MkDocs sites for different languages are stored.
- **Site**: An individual MkDocs site for a specific language within the project.

### Notes

- Ensure the specified project path is correct and accessible.
- You can update the GitHub account information in `mkdocs-lang.yml` later using the `config` action. 