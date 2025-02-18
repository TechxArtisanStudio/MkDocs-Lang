import argparse
import logging
import os
from mkdocs_lang.actions import newproject, config, addsite, run, newsite, removesite, copy, delete, git
from mkdocs_lang.utils import analyze_project_structure, validate_and_analyze_project_path
from mkdocs_lang.logging_config import setup_logging  # Import the logging setup

def setup_parser():
    parser = argparse.ArgumentParser(description='Manage multi-language MkDocs projects.')
    subparsers = parser.add_subparsers(dest='action')

    # NewProject action
    newproject_parser = subparsers.add_parser('newproject', help='Create a new project folder with a mkdocs-lang.yml file.')
    newproject_parser.add_argument('--project', '-p', required=True, help='Path to the new project')
    newproject_parser.add_argument('--github', '-g', help='GitHub account for repository URLs')

    # New action
    newsite_parser = subparsers.add_parser('newsite', help='Create a new MkDocs project.')
    newsite_parser.add_argument('mkdocs_project', help='Name of the MkDocs project')
    newsite_parser.add_argument('--lang', '-l', default='en', help='Language code for the MkDocs project')
    newsite_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')

    # Config action
    config_parser = subparsers.add_parser('config', help='Update configuration for the main project.')
    config_parser.add_argument('--project', '-p', help='Path to the main project')
    config_parser.add_argument('--github', '-g', required=True, help='New GitHub account for repository URLs')

    # Addsite action
    addsite_parser = subparsers.add_parser('addsite', help='Clone a GitHub repository into the main project.')
    addsite_parser.add_argument('url_repo', nargs='?', help='URL of the GitHub repository to clone')
    addsite_parser.add_argument('--lang', '-l', default='en', help='Language code for the MkDocs project')
    addsite_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    addsite_parser.add_argument('--batch', '-b', nargs='?', const=True, help='Path to a file containing multiple repositories to clone')
    addsite_parser.add_argument('--dry-run', '-d', action='store_true', help='Add repository to repos.txt without cloning')

    # Custom Command Line action
    cl_parser = subparsers.add_parser('run', help='Execute a custom command across all MkDocs projects.')
    cl_parser.add_argument('command', help='The custom command to execute')
    cl_parser.add_argument('relative_path', nargs='?', default=None, help='Relative path within MkDocs sites')
    cl_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    cl_parser.add_argument('-y', action='store_true', help='Automatically confirm execution without prompting')

    # RemoveSite action
    removesite_parser = subparsers.add_parser('removesite', help='Remove a MkDocs site from the main project.')
    removesite_parser.add_argument('site_name', help='Name of the MkDocs site to remove')
    removesite_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')

    # Copy action
    copy_parser = subparsers.add_parser('copy', help='Copy a file or folder across all MkDocs projects.')
    copy_parser.add_argument('source', help='Path to the file or folder to copy')
    copy_parser.add_argument('relative_path', nargs='?', default=None, help='Relative path within MkDocs sites')
    copy_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    copy_parser.add_argument('--dir', '-d', action='store_true', help='Indicate if the source is a directory')
    copy_parser.add_argument('-y', action='store_true', help='Automatically confirm execution without prompting')
    copy_parser.add_argument('--force', '-f', action='store_true', help='Overwrite existing files without prompting')
    copy_parser.add_argument('--backup', '-b', action='store_true', help='Create a backup of existing files before overwriting')

    # Delete action
    del_parser = subparsers.add_parser('del', help='Delete a file or folder across all MkDocs projects.')
    del_parser.add_argument('target', help='Path to the file or folder to delete')
    del_parser.add_argument('relative_path', nargs='?', default=None, help='Relative path within MkDocs sites')
    del_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    del_parser.add_argument('--dir', '-d', action='store_true', help='Indicate if the target is a directory')
    del_parser.add_argument('-y', action='store_true', help='Automatically confirm execution without prompting')

    # Git action
    git_parser = subparsers.add_parser('git', help='Execute a git command across all MkDocs projects.')
    git_parser.add_argument('git_command', help='The git command to execute (e.g., "status", "pull")')
    git_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    git_parser.add_argument('-y', action='store_true', help='Automatically confirm execution without prompting')

    return parser

def log_action_start(action_name, details):
    logging.info(f"----- Starting '{action_name}' -----")
    logging.info(f"Details: {details}")
    logging.info(f"Current working directory: {os.getcwd()}")

def log_action_end(action_name):
    logging.info(f"******* Finished '{action_name}' *******")

def handle_newproject(args):
    log_action_start('newproject', f"project path: {args.project}, GitHub account: {args.github}")
    newproject.create_project(args.project, args.github)
    log_action_end('newproject')

def handle_newsite(args, main_project_path):
    log_action_start('newsite', f"project name: {args.mkdocs_project}, language: {args.lang}, path: {main_project_path}")
    newsite.create_mkdocs_project(args.mkdocs_project, args.lang, main_project_path)
    log_action_end('newsite')

def handle_config(args, main_project_path):
    log_action_start('config', f"GitHub account: {args.github}, path: {main_project_path}")
    config.update_github_account(main_project_path, args.github)
    log_action_end('config')

def handle_addsite(args, main_project_path):
    log_action_start('addsite', f"URL: {args.url_repo}, language: {args.lang}, path: {main_project_path}")
    if args.batch is not None:
        batch_file = args.batch if isinstance(args.batch, str) else None
        addsite.clone_repos_from_file(batch_file, main_project_path)
    elif args.url_repo:
        addsite.clone_repo(args.url_repo, args.lang, main_project_path, args.dry_run)
    else:
        addsite.clone_repos_from_mkdocs_lang(main_project_path)
    log_action_end('addsite')

def handle_run(args, main_project_path):
    log_action_start('run', f"command: {args.command}, relative path: {args.relative_path}, path: {main_project_path}")
    run.execute_command(args.command, args.relative_path, main_project_path, args.y)
    log_action_end('run')

def handle_removesite(args, main_project_path):
    log_action_start('removesite', f"site name: {args.site_name}, path: {main_project_path}")
    removesite.remove_site(args.site_name, main_project_path)
    log_action_end('removesite')

def handle_copy(args, main_project_path):
    log_action_start('copy', f"source: {args.source}, relative path: {args.relative_path}, path: {main_project_path}")
    copy.copy_item(args.source, args.relative_path, main_project_path, args.dir, args.y, args.force, args.backup)
    log_action_end('copy')

def handle_delete(args, main_project_path):
    log_action_start('delete', f"target: {args.target}, relative path: {args.relative_path}, path: {main_project_path}")
    delete.delete_item(args.target, args.relative_path, main_project_path, args.dir, args.y)
    log_action_end('delete')

def handle_git(args, main_project_path):
    log_action_start('git', f"command: {args.git_command}, path: {main_project_path}")
    git.execute_git_command(args.git_command, main_project_path, args.y)
    log_action_end('git')

def main(args=None):
    parser = setup_parser()
    args = parser.parse_args(args)

    # Determine the log directory based on the project path
    if args.project:
        log_dir = os.path.join(args.project, 'log')
    else:
        main_project_path, _, _ = analyze_project_structure()
        log_dir = os.path.join(main_project_path, 'log') if main_project_path else 'log'

    # Setup logging
    setup_logging(log_dir)  # Initialize logging configuration with the log directory

    if args.action == 'newproject':
        handle_newproject(args)
        return

    # Use the specified project path if provided
    if args.project:
        main_project_path, is_inside_mkdocs_website, combined_paths = validate_and_analyze_project_path(args.project)
    else:
        # Analyze the project structure from the current directory
        main_project_path, is_inside_mkdocs_website, combined_paths = analyze_project_structure()

    if main_project_path is None:
        logging.error("mkdocs-lang.yml not found. Please specify the --project path.")
        return

    # Pass the main_project_path and other outputs to each action
    action_handlers = {
        'newsite': handle_newsite,
        'config': handle_config,
        'addsite': handle_addsite,
        'run': handle_run,
        'removesite': handle_removesite,
        'copy': handle_copy,
        'del': handle_delete,
        'git': handle_git
    }

    if args.action in action_handlers:
        action_handlers[args.action](args, main_project_path)
    else:
        logging.error("Unknown action: %s", args.action)

if __name__ == '__main__':
    main()
