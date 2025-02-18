## Copy Files or Folders Across MkDocs Projects

The `copy` action allows you to copy a file or folder across all MkDocs websites within your project setup.

### Usage

```bash
mklang copy <source-path> [relative-path] [options]
# or using short options
mklang copy <source-path> [relative-path] -p <path-to-main-project> -d -f -b
```

### Options

- `<source-path>`: The path to the file or folder you want to copy. This can be an absolute or relative path.
- `[relative-path]`: An optional relative path within each MkDocs site where the file or folder should be copied. If not specified, the default behavior is to maintain the source's relative path.
- `--project`, `-p`: Specify the path to the main project if not in the current directory.
- `--dir`, `-d`: Indicate if the source is a directory. Use this flag when copying directories.
- `-y`: Automatically confirm execution without prompting for user confirmation.
- `--force`, `-f`: Overwrite existing files without prompting. Use this flag to avoid manual confirmation for overwriting files.
- `--backup`, `-b`: Create a backup of existing files before overwriting.

### What It Does

1. **Determines the Main Project Path**: Uses a utility function to find the main project path.
2. **Validates Source Path**: Ensures the source path exists and is accessible.
3. **Copies Files/Folders**: Copies the specified file or folder to each MkDocs site.
4. **Handles Overwrites and Backups**: Manages overwriting existing files and creating backups if specified.
5. **Logs the Action**: Records the action details and any errors in the `log/` directory.

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
- Check the `log/` directory for detailed logs of the action, including any errors encountered during the process. 