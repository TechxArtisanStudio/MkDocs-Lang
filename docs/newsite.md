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

### What It Does

1. **Validates the Language Code**: Ensures the provided language code is supported.
2. **Determines the Main Project Path**: Reads the main project path and GitHub account from `mkdocs-lang.yml`.
3. **Creates a New MkDocs Site**: Uses the MkDocs executable from the virtual environment to create a new site directory.
4. **Updates Configuration Files**:
   - Updates `mkdocs.yml` with a template.
   - Adds the new site to `mkdocs-lang.yml`.
5. **Logs the Action**: Records the action details and any errors in the `log/` directory.

### Example

To create a new site named `mk-website_es` for Spanish in your project, you would run:

```bash
mklang new mk-website_es --project /path/to/website-project --lang es
```

This command will:
- Create a new directory named `mk-website_es` in the main project path.
- Add an entry for `mk-website_es` in the `mkdocs-lang.yml` configuration file.
- Log the action and any errors encountered during the process.

### Notes

- Ensure the `mkdocs-lang.yml` file is correctly configured before adding a new site.
- The `newsite` action will not affect any existing sites or configurations within your project.
- Supported language codes are based on MkDocs Material's supported languages.
- Check the `log/` directory for detailed logs of the action, including any errors encountered during the process. 