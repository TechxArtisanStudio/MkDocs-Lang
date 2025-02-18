# Update Project Configuration

The `config` action allows you to update configuration settings for your MkDocs multi-language project. This is particularly useful for updating the GitHub account information stored in the `mkdocs-lang.yml` file.

## Usage

```bash
mklang config --github <github-account> --project /path/to/main-project
# or using short options
mklang config -g <github-account> -p /path/to/main-project
```

## Options

- `--github`, `-g`: Specify the new GitHub account to be updated in the `mkdocs-lang.yml` file.
- `--project`, `-p`: Specify the path to the main project directory where the `mkdocs-lang.yml` file is located.

## What It Does

1. **Determines the Main Project Path**: Uses a utility function to find the main project path.
2. **Checks Configuration**: Ensures `mkdocs-lang.yml` exists and reads its content.
3. **Updates GitHub Account**: Modifies the GitHub account information in the `mkdocs-lang.yml` file.
4. **Logs the Action**: Records the action details and any errors in the `log/` directory.

## Examples

1. **Update GitHub Account**

   ```bash
   mklang config --github new-github-account --project /path/to/main-project
   ```

2. **Using Short Options**

   ```bash
   mklang config -g new-github-account -p /path/to/main-project
   ```

## Notes

- Ensure the `mkdocs-lang.yml` file is present in the specified project directory.
- The `config` action only updates the GitHub account information; other configurations remain unchanged.
- Check the `log/` directory for detailed logs of the action, including any errors encountered during the process. 