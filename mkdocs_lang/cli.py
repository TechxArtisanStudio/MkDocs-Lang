import argparse
from mkdocs_lang.actions import newproject, config, addsite, cl, newsite, removesite
import os

def main(args=None):
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

    # addsite action
    addsite_parser = subparsers.add_parser('addsite', help='Clone a GitHub repository into the main project.')
    addsite_parser.add_argument('url_repo', nargs='?', help='URL of the GitHub repository to clone')
    addsite_parser.add_argument('--lang', '-l', default='en', help='Language code for the MkDocs project')
    addsite_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    addsite_parser.add_argument('--batch', '-b', help='Path to a file containing multiple repositories to clone')
    addsite_parser.add_argument('--dry-run', '-d', action='store_true', help='Add repository to mkdocs-lang.yml without cloning')

    # Custom Command Line action
    cl_parser = subparsers.add_parser('cl', help='Execute a custom command across all MkDocs projects.')
    cl_parser.add_argument('command', help='The custom command to execute')
    cl_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')
    cl_parser.add_argument('-y', action='store_true', help='Automatically confirm execution without prompting')

    # RemoveSite action
    removesite_parser = subparsers.add_parser('removesite', help='Remove a MkDocs site from the main project.')
    removesite_parser.add_argument('site_name', help='Name of the MkDocs site to remove')
    removesite_parser.add_argument('--project', '-p', help='Path to the main project if not in current directory')

    # Parse arguments
    args = parser.parse_args(args)

    if args.action == 'newproject':
        newproject.create_project(args.project, args.github)
    elif args.action == 'newsite':
        newsite.create_mkdocs_project(args.mkdocs_project, args.lang, args.project)
    elif args.action == 'config':
        config.update_github_account(args.project, args.github)
    elif args.action == 'addsite':
        if args.batch:
            addsite.clone_repos_from_file(args.batch, args.project)
        elif args.url_repo:
            addsite.clone_repo(args.url_repo, args.lang, args.project, args.dry_run)
        else:
            addsite.clone_repos_from_mkdocs_lang(args.project)
    elif args.action == 'cl':
        cl.execute_command(args.command, args.project, args.y)
    elif args.action == 'removesite':
        removesite.remove_site(args.site_name, args.project)

if __name__ == '__main__':
    main()
