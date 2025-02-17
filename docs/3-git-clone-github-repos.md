## Add GitHub Repositories

The `gitclone` action clones an existing GitHub repository into your MkDocs project setup.

#### Usage

```bash
mklang gitclone <repo-url> --lang <language-code> --project <path-to-main-project>
```

- `repo-url` can be in SSH or HTTPS format.
- `--lang` specifies the language code for the site.

#### What It Does

1. Clones the specified GitHub repository into the main project directory.
2. Updates `mkdocs-lang.yml` with the new site's details.
3. Converts the `repo_url` to HTTPS format in `mkdocs-lang.yml`.

#### Example

To clone a repository:

```bash
mklang gitclone git@github.com:TechxArtisanStudio/Openterface.git --lang en --project /path/to/mkdocs-project
``` 