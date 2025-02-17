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
- `--backup`, `-b`: Create a backup of existing files before overwriting.

### Examples

1. **Copy a File to a Specific Subdirectory**

   ```bash
   mklang copy /path/to/file.txt docs/subdir --project /path/to/main-project
   ```

2. **Copy a Directory Across All Sites**

   ```bash
   mklang copy /path/to/assets --dir -y --project /path/to/main-project
   ```

3. **Copy a File and Create Backups of Existing Files**

   ```bash
   mklang copy /path/to/config.yml --backup --project /path/to/main-project
   ```

### Notes

- Ensure that the source path is correct and accessible.
- Use the `--force` flag with caution, as it will overwrite existing files without further confirmation.
- The `--backup` option is useful for preserving the current state of files before making changes. 