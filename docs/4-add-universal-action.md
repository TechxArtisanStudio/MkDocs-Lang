## Universal Command Line Action

The `cl` action allows you to execute a custom command across all MkDocs sites within a specified directory structure.

#### Usage

```bash
mklang cl "<the-customized-command-line>" --project /path/to/website-project
```

#### Examples

1. **Git Pull Across All Sites**

   ```bash
   mklang cl "git pull" --project /path/to/website-project
   ```

2. **Create a File in Each Site's Subdirectory**

   ```bash
   mklang cl "touch index.md"
   ```

3. **Auto-Detection of Main Project Path**

   ```bash
   mklang cl "touch blog-1.md"
   ```

#### Optimization

The `cl` action is optimized to detect the main project path automatically, so you don't need to specify `--project` if you are within a subdirectory of a MkDocs site. 