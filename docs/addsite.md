## Add a New MkDocs Site

The `addsite` action allows you to add a new MkDocs site to your project by cloning a Git repository.

### Usage

```bash
mklang addsite <url-repo> [options]
# or using the manage.py script
python manage.py addsite <url-repo> [options]
```

### Options

- `<url-repo>`: The URL of the Git repository to clone.
- `--lang`, `-l`: Specify the language code for the MkDocs project. Defaults to `en`.
- `--project`, `-p`: Specify the path to the main project if not in the current directory.
- `--batch`, `-b`: Path to a file containing multiple repositories to clone.
- `--dry-run`, `-d`: Add the repository to `mkdocs-lang.yml` without cloning.

### Examples

1. **Clone a Single Repository**

   ```bash
   mklang addsite git@github.com:username/repo.git --project /path/to/main-project
   ```

2. **Clone Multiple Repositories from a File**

   ```bash
   mklang addsite --batch /path/to/repos.txt --project /path/to/main-project
   ```

3. **Add a Repository Without Cloning**

   ```bash
   mklang addsite git@github.com:username/repo.git --dry-run --project /path/to/main-project
   ```

### Notes

- Ensure that the repository URL is correct and accessible.
- The `--batch` option allows you to specify a file with multiple repositories, each on a new line.
- The `--dry-run` option is useful for testing changes to `mkdocs-lang.yml` without making any network requests. 