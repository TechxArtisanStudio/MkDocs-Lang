cd /home/project && mklang newproject --project op-website --github TechxArtisan && cd op-website && ls && cat mkdocs-lang.yml

mklang addsite git@github.com:TechxArtisanStudio/Openterface --lang en

mklang addsite git@github.com:TechxArtisanStudio/Openterface_jp --lang ja -d
mklang addsite git@github.com:TechxArtisanStudio/Openterface_zh --lang zh -d

ls && cat mkdocs-lang.yml && cat repos.txt

mklang addsite -b

----

cat /home/project/op-website/log/mklang.log

----

cd /home/project/op-website && mklang newsite Openterface_fr --lang fr

mklang removesite Openterface_fr

---

cd /home/project/op-website/Openterface/
mklang run "touch test.md"

cd /home/project/op-website/Openterface/docs/blog/ && mklang run "touch test.md"

mklang del test.md

---

cd /home/project/op-website/Openterface/docs/blog/ && touch test.md && mklang copy test.md
mklang del test.md

---

mklang git status