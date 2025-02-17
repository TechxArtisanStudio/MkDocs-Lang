## Universal Command Line Action

The `run` action allows you to execute a custom command across all MkDocs sites within a specified directory structure.

#### Usage

```bash
mklang run "<the-customized-command-line>" --project /path/to/website-project
# or using short options
mklang run "<the-customized-command-line>" -p /path/to/website-project
```

#### Examples

1. **Git Pull Across All Sites**

   ```bash
   mklang run "git pull" --project /path/to/website-project
   # or using short options
   mklang run "git pull" -p /path/to/website-project
   ```

2. **Create a File in Each Site's Subdirectory**

   ```bash
   mklang run "touch index.md"
   ```

3. **Auto-Detection of Main Project Path**

   ```bash
   mklang run "touch blog-1.md"
   ```

#### Optimization

The `run` action is optimized to detect the main project path automatically, so you don't need to specify `--project` if you are within a subdirectory of a MkDocs site. 