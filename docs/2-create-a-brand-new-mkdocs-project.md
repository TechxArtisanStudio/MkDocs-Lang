### 2. Create a Brand New MkDocs Site

The `new` action adds a new MkDocs site to your multi-language setup.

#### Usage

```bash
mklang new <mkdocs-site> --project <path-to-the-mainproject> --lang <language-code>
```

- `--lang` defaults to `en`.

#### Language Code Examples

Here are some examples of language codes supported by MkDocs Material:

- `en` for English
- `fr` for French
- `de` for German
- `zh` for Chinese (Simplified)
- `es` for Spanish

For a full list of supported languages and more details, visit the [MkDocs Material Language Setup](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/).

#### What It Does

1. Fetches the main project path from `mkdocs-lang.yml`.
2. Creates a new MkDocs site directory.
3. Updates `mkdocs.yml` using the `mkdocs.yml.template`.
4. Adds the new site to `mkdocs-lang.yml`.

#### Project Structure

After running the command, your project directory will include:

```
/website-project/
├── mkdocs-lang.yml
├── mkdocs-site/
│   ├── docs/
│   ├── mkdocs.yml
```