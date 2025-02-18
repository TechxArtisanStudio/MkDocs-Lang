action `run` may be called in any deep level of a mkdocs website of the main project.

## Case_1:

we may run:
```
mkland run "touch blog-1.md"
```
at the path of "/home/project/openterface-website/site/Openterface/docs/blog/posts", which is expected to run iterativly for below path
"
/home/project/openterface-website/site/Openterface/docs/blog/posts
/home/project/openterface-website/site/Openterface_jp/docs/blog/posts
/home/project/openterface-website/site/Openterface_zh/docs/blog/posts
"
if we have these 3 mkdocs websites in the main project.

## Case_2:

if we run:
```
mkland run "touch post-a.md" docs/
```
with [relative-path] specified, then use the relative path.
which means, run iterativly for below path:
"
/home/project/openterface-website/site/Openterface/docs
/home/project/openterface-website/site/Openterface_jp/docs
/home/project/openterface-website/site/Openterface_zh/docs
"

please keep in mind that [relative-path] is related to the root of each mkdocs website.

## Case_3:

if we run:
```
mkland run "touch post-a.md" docs/ -p /path/to/website-project
```
it will do the same job as above Case_2.

just keep in mind that with `--project` specified, it will try to get `mkdocs-lang.yml` at this path.

Otherwise, without `--project` specified, just like Case_1 and Case_2, it will use method from `utils.py` to traverse up to the root to find `mkdocs-lang.yml`.