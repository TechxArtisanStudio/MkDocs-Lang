## Copy Files or Folders Across MkDocs Projects

The `copy` action allows you to copy a file or folder across all MkDocs websites within your project setup.

### Usage

```bash
mklang copy <source-path> [relative-path] [options]
# or using the manage.py script
python manage.py copy <source-path> [relative-path] [options]
```

### Options

- `<source-path>`: The path to the file or folder you want to copy. This can be an absolute or relative path.
- `[relative-path]`: An optional relative path within each MkDocs site where the file or folder should be copied. If not specified, the default behavior is to maintain the source's relative path.
- `--project`, `-p`: Specify the path to the main project if not in the current directory.
- `--dir`, `-d`: Indicate if the source is a directory. Use this flag when copying directories.
- `-y`: Automatically confirm execution without prompting for user confirmation.
- `--force`, `-f`: Overwrite existing files without prompting. Use this flag to avoid manual confirmation for overwriting files.
- `--backup`, `-b`: Create a backup of existing files before overwriting. The backup will have a `.bak` suffix.

### What It Does

1. Validates the source path to ensure it exists.
2. Determines the main project path, either from the provided `--project` option or by traversing up the directory tree.
3. Copies the specified file or folder to each MkDocs website directory listed in `mkdocs-lang.yml`.
4. If a `relative-path` is specified, it is used to determine the target location within each MkDocs site.
5. Provides options to handle overwrites and create backups of existing files.

### Example

To copy a file named `blog-1.md` to all MkDocs websites:

```bash
mklang copy /path/to/blog-1.md --project /path/to/main-project
# or using the manage.py script
python manage.py copy /path/to/blog-1.md --project /path/to/main-project
```

To copy a file to a specific relative path within each MkDocs site:

```bash
mklang copy /path/to/blog-1.md docs/ --project /path/to/main-project
# or using the manage.py script
python manage.py copy /path/to/blog-1.md docs/ --project /path/to/main-project
```

To copy a directory named `assets` and automatically confirm the operation:

```bash
mklang copy /path/to/assets --dir -y --project /path/to/main-project
# or using the manage.py script
python manage.py copy /path/to/assets --dir -y --project /path/to/main-project
```

To copy a file and create backups of existing files:

```bash
mklang copy /path/to/config.yml --backup --project /path/to/main-project
# or using the manage.py script
python manage.py copy /path/to/config.yml --backup --project /path/to/main-project
```

### Notes

- Ensure that the source path is correct and accessible.
- Use the `--force` flag with caution, as it will overwrite existing files without further confirmation.
- The `--backup` option is useful for preserving the current state of files before making changes. 