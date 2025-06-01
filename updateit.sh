#!/bin/bash  
echo "$1"
python assets/DependencyGraph.py
bash -c 'rm -f *.aux *.log *.out *.toc *.bbl *.dvi *.ist *.blg *.fls *.fdb_latexmk *.synctex.gz *.glo *.gls *.glg *.*-glg *.*-gls *.*-glo'
git add . 
git commit -m "$1"
git push origin main 