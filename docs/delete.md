## Delete Files or Folders Across MkDocs Projects

The `delete` action allows you to delete a file or folder across all MkDocs websites within your project setup.

### Usage

```bash
mklang del <target-path> [relative-path] [options]
# or using the manage.py script
python manage.py del <target-path> [relative-path] [options]
```

### Options

- `<target-path>`: The path to the file or folder you want to delete. This can be an absolute or relative path.
- `[relative-path]`: An optional relative path within each MkDocs site where the file or folder should be deleted. If not specified, the default behavior is to use the current directory relative to each MkDocs site.
- `--project`, `-p`: Specify the path to the main project if not in the current directory.
- `--dir`, `-d`: Indicate if the target is a directory. Use this flag when deleting directories.
- `-y`: Automatically confirm execution without prompting for user confirmation.

### Examples

1. **Delete a File from a Specific Subdirectory**

   ```bash
   mklang del /path/to/file.txt docs/subdir --project /path/to/main-project
   ```

2. **Delete a Directory Across All Sites**

   ```bash
   mklang del /path/to/assets --dir -y --project /path/to/main-project
   ```

3. **Delete a File Using Auto-Detection of Main Project Path**

   ```bash
   mklang del blog-1.md
   ```

### Notes

- Ensure that the target path is correct and accessible.
- Use the `--dir` flag when deleting directories to ensure the correct operation.
- The `-y` option is useful for automating the deletion process without manual confirmation. 