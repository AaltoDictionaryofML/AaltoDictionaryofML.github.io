#!/bin/bash  
echo "$1"
python assets/FlattenGlossary.py
python assets/DependencyGraph.py
bash -c 'rm -f *.aux *.log *.out *.toc *.bbl *.dvi *.ist *.blg *.fls *.fdb_latexmk *.synctex.gz *.glo *.gls *.glg *.*-glg *.*-gls *.*-glo'
git add . 
git commit -m "$1"
git push origin main 

# --- Backup section (existing cloned repo) ---
BACKUP_DIR="$HOME/adictmlbackup"

echo "Backing up selected files into backup repo at $BACKUP_DIR ..."

# Files/directories to back up (customize as needed)
FILES_TO_BACKUP=(
    "ADictML_English.tex"
    "ADictML_Glossary_English.tex"
    "ListSymbols_English.tex"
    "assets/ml_macros.tex"
    "assets/Literature.bib"
)

for item in "${FILES_TO_BACKUP[@]}"; do
    if [ -e "$item" ]; then
        cp -R "$item" "$BACKUP_DIR/"
        echo "  → Copied: $item"
    else
        echo "  → Skipped (not found): $item"
    fi
done

# --- Commit & push inside the backup repo ---
echo "Committing inside backup repository..."

(
    cd "$BACKUP_DIR"
    git add .
    git commit -m "Backup: $MSG" || echo "No changes to commit in backup repo."
    git push
)

echo "Backup repo updated."