# Git Action

The `git` action allows you to execute git commands across all MkDocs sites within your main project directory. This is useful for managing multiple repositories simultaneously.

## Usage

You can use the `git` action in two ways:

1. **From the main project directory:**

   ```bash
   python manage.py git <git-command> --project /path/to/main/project
   ```

   Replace `<git-command>` with the desired git command, such as `status` or `pull`.

2. **From within any MkDocs site directory:**

   ```bash
   mklang git <git-command>
   ```

   The script will automatically traverse up to find the `mkdocs-lang.yml` file and determine the main project path.

## Options

- `--project`, `-p`: Specify the path to the main project if not running from within a MkDocs site.
- `-y`: Automatically confirm execution without prompting for confirmation.

## Examples

- Check the status of all repositories:

  ```bash
  python manage.py git status --project /home/project/op-website/
  ```

- Pull the latest changes for all repositories:

  ```bash
  mklang git pull
  ```

- Sync changes with a commit message:

  ```bash
  python manage.py git sync "Update documentation" --project /home/project/op-website/
  ```

## Notes

- The command will be executed at the root of each MkDocs site, not in subdirectories.
- Ensure you have the necessary permissions and SSH keys set up for git operations. 