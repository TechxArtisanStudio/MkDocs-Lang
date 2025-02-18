cd /home/project && mklang newproject --project op-website --github TechxArtisan && cd op-website && ls && cat mkdocs-lang.yml

mklang addsite git@github.com:TechxArtisanStudio/Openterface --lang en

mklang addsite git@github.com:TechxArtisanStudio/Openterface_jp --lang ja -d
mklang addsite git@github.com:TechxArtisanStudio/Openterface_zh --lang zh -d

ls && cat mkdocs-lang.yml && cat repos.txt

mklang addsite -b

----

cd /home/project/op-website && mklang newsite Openterface_fr --lang fr

---

