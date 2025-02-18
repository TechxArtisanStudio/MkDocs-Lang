# Test Script for mklang Actions

## Setup and Initialization
```bash
cd /home/project && mklang newproject --project op-website --github TechxArtisan
cd op-website
```

# Verify project creation
```bash
ls
cat mkdocs-lang.yml
```

## Adding Sites
# Add English site
```bash
mklang addsite git@github.com:TechxArtisanStudio/Openterface --lang en
```

# Add Japanese and Chinese sites with draft flag
```bash
mklang addsite git@github.com:TechxArtisanStudio/Openterface_jp --lang ja -d
mklang addsite git@github.com:TechxArtisanStudio/Openterface_zh --lang zh -d
```

# Verify sites added
```bash
ls
cat mkdocs-lang.yml
cat repos.txt
```

## Test Default Branch Addition
```bash
mklang addsite -b
```

## Log Verification
# Check logs for any errors or warnings
```bash
cat /home/project/op-website/log/mklang.log
```

## Site Management
# Add and remove a French site
```bash
cd /home/project/op-website
mklang newsite Openterface_fr --lang fr
mklang removesite Openterface_fr
```

## File Operations
# Create and delete a test file
```bash
cd /home/project/op-website/Openterface/
mklang run "touch test.md"
```

```bash
cd /home/project/op-website/Openterface/docs/blog/
mklang run "touch test.md"
mklang del test.md
```

## Copy and Delete Operations
# Test copy and delete functionality
```bash
cd /home/project/op-website/Openterface/docs/blog/
touch test.md
mklang copy test.md
mklang del test.md
```

## Batch Operations
# Batch add sites
```bash
mklang addsite git@github.com:TechxArtisanStudio/Openterface_es --lang es
mklang addsite git@github.com:TechxArtisanStudio/Openterface_it --lang it
```

# Batch remove sites
```bash
mklang removesite Openterface_es
mklang removesite Openterface_it
```

# Batch copy operation
```bash
mklang copy /path/to/shared/resource.md --project /home/project/op-website
```

# Batch delete operation
```bash
mklang del /path/to/shared/resource.md --project /home/project/op-website
```

## Batch Git Operations
# Run git status across all sites
```bash
mklang git "status" --project /home/project/op-website
```

## Run Action Tests
# Case 1: Run command at a deep level
```bash
cd /home/project/openterface-website/site/Openterface/docs/blog/posts
mklang run "touch blog-1.md"
```

# Case 2: Run command with relative path
```bash
cd /home/project/openterface-website/site/Openterface
mklang run "touch post-a.md" docs/
```

# Case 3: Run command with project path specified
```bash
mklang run "touch post-a.md" docs/ -p /home/project/openterface-website
```

# End of Test Script 