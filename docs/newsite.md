# Create a New MkDocs Site

The `newsite` action allows you to add a new MkDocs site to your multi-language project setup. This action will create a new site directory and update the `mkdocs-lang.yml` configuration file to include the new site entry.

## Usage

To create a new MkDocs site, use the following command:

```bash
mklang new <mkdocs-site> --project <path-to-the-mainproject> --lang <language-code>
# or using short options
mklang new <mkdocs-site> -p <path-to-the-mainproject> -l <language-code>
```

### Parameters

- `<mkdocs-site>`: The name of the new MkDocs site you want to create.
- `--project` or `-p`: The path to the main project directory where the `mkdocs-lang.yml` file is located.
- `--lang` or `-l`: The language code for the new site. Defaults to `en` if not specified.

### Example

To create a new site named `mk-website_es` for Spanish in your project, you would run:

```bash
mklang new mk-website_es --project /path/to/website-project --lang es
```

This command will:
- Create a new directory named `mk-website_es` in the main project path.
- Add an entry for `mk-website_es` in the `mkdocs-lang.yml` configuration file.

### Notes

- Ensure the `mkdocs-lang.yml` file is correctly configured before adding a new site.
- The `newsite` action will not affect any existing sites or configurations within your project. 