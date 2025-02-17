# Remove a MkDocs Site

The `removesite` action allows you to remove an existing MkDocs site from your multi-language project setup. This action will delete the site directory and update the `mkdocs-lang.yml` configuration file to remove the site entry.

## Usage

To remove a MkDocs site, use the following command:

```bash
mklang removesite <site-name> --project <path-to-main-project>
# or using short options
mklang removesite <site-name> -p <path-to-main-project>
```

### Parameters

- `<site-name>`: The name of the MkDocs site you want to remove.
- `--project` or `-p`: The path to the main project directory where the `mkdocs-lang.yml` file is located.

### Example

To remove a site named `mk-website_fr` from your project, you would run:

```bash
mklang removesite mk-website_fr --project /path/to/website-project
```

This command will:
- Delete the `mk-website_fr` directory from the main project path.
- Remove the `mk-website_fr` entry from the `mkdocs-lang.yml` configuration file.

### Notes

- Ensure you have a backup of your data before removing a site, as this action is irreversible.
- The `removesite` action will not affect any other sites or configurations within your project. 