## Universal Command Line Action

The `run` action allows you to execute a custom command across all MkDocs sites within a specified directory structure.

### Usage

```bash
mklang run "<the-customized-command-line>" [relative-path] --project /path/to/website-project
# or using short options
mklang run "<the-customized-command-line>" [relative-path] -p /path/to/website-project
```

### Options

- `<the-customized-command-line>`: The command you want to execute in each MkDocs site.
- `[relative-path]`: An optional relative path within each MkDocs site where the command should be executed. If not specified, the command will be executed in the current directory relative to each MkDocs site.
- `--project`, `-p`: Specify the path to the main project if not in the current directory.
- `-y`: Automatically confirm execution without prompting for user confirmation.

### What It Does

1. **Determines the Main Project Path**: Uses a utility function to find the main project path.
2. **Validates Command**: Ensures the command is valid and executable.
3. **Executes Command**: Runs the specified command in each MkDocs site directory.
4. **Logs the Action**: Records the action details, output, and any errors in the `log/` directory.

### Examples

1. **Git Pull Across All Sites**

   ```bash
   mklang run "git pull" --project /path/to/website-project
   # or using short options
   mklang run "git pull" -p /path/to/website-project
   ```

2. **Create a File in Each Site's Subdirectory**

   ```bash
   mklang run "touch index.md" docs/blog/posts --project /path/to/website-project
   ```

3. **Auto-Detection of Main Project Path**

   ```bash
   mklang run "touch blog-1.md"
   ```

### Notes

- Ensure the command is valid and executable in the context of each MkDocs site.
- The `-y` option is useful for automating the execution process without manual confirmation.
- Check the `log/` directory for detailed logs of the action, including any output and errors encountered during the process.

### Optimization

The `run` action is optimized to detect the main project path automatically, so you don't need to specify `--project` if you are within a subdirectory of a MkDocs site. The command will be executed in the corresponding relative path for all MkDocs sites. 