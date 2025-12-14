#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./updateit.sh "your commit message"
# Optional env vars:
#   BACKUP_DIR=~/adictmlbackup
#   BACKUP_MODE=rsync   # or: cp
#   BACKUP_KEEP_DAYS=30 # delete old timestamped backups (only for timestamp mode)
#   BACKUP_LAYOUT=mirror  # or: timestamp
#
# What it does:
#  1) runs your Python scripts
#  2) cleans LaTeX junk
#  3) commits & pushes main repo
#  4) backs up ALL TeX files starting with ADictML* (plus a few key assets)
#  5) commits & pushes the backup repo

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "ERROR: commit message missing."
  echo "Usage: $0 \"commit message\""
  exit 1
fi

BACKUP_DIR="${BACKUP_DIR:-$HOME/adictmlbackup}"
BACKUP_MODE="${BACKUP_MODE:-rsync}"     # rsync | cp
BACKUP_LAYOUT="${BACKUP_LAYOUT:-mirror}" # mirror | timestamp
BACKUP_KEEP_DAYS="${BACKUP_KEEP_DAYS:-30}"

echo "[INFO] Commit message: $MSG"
echo "[INFO] Backup repo: $BACKUP_DIR"
echo "[INFO] Backup mode: $BACKUP_MODE"
echo "[INFO] Backup layout: $BACKUP_LAYOUT"

# --- Sanity checks ---
command -v python >/dev/null 2>&1 || { echo "ERROR: python not found in PATH"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "ERROR: git not found in PATH"; exit 1; }

if [[ ! -d "$BACKUP_DIR/.git" ]]; then
  echo "ERROR: BACKUP_DIR does not look like a git repo: $BACKUP_DIR"
  echo "Tip: git clone <your-backup-remote> \"$BACKUP_DIR\""
  exit 1
fi

# --- Run your generation scripts ---
echo "[INFO] Running FlattenGlossary.py ..."
python assets/FlattenGlossary.py

echo "[INFO] Running DependencyGraph.py ..."
python assets/DependencyGraph.py

# --- Clean LaTeX junk (flexible + safe) ---
echo "[INFO] Cleaning LaTeX temporary files ..."
find . -maxdepth 2 -type f \( \
  -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o \
  -name "*.bbl" -o -name "*.blg" -o -name "*.dvi" -o -name "*.ist" -o \
  -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.synctex.gz" -o \
  -name "*.glo" -o -name "*.gls" -o -name "*.glg" -o \
  -name "*-glg" -o -name "*-gls" -o -name "*-glo" \
\) -print -delete

# --- Commit & push main repo ---
echo "[INFO] Committing in main repo ..."
git add -A
git commit -m "$MSG" || echo "[INFO] No changes to commit in main repo."
git push origin main

# --- Backup selection ---
# All TeX files starting with ADictML* + a few important extras
# (Edit EXTRAS if you want.)
mapfile -d '' TEX_FILES < <(find . -maxdepth 1 -type f -name 'ADictML*.tex' -print0 | sort -z)

EXTRAS=(
  "ListSymbols_English.tex"
  "assets/ml_macros.tex"
  "assets/Literature.bib"
)

# Filter extras to existing files
EXTRAS_EXISTING=()
for f in "${EXTRAS[@]}"; do
  [[ -e "$f" ]] && EXTRAS_EXISTING+=("$f")
done

if [[ "${#TEX_FILES[@]}" -eq 0 ]]; then
  echo "[WARN] No files matched ADictML*.tex in repo root."
else
  echo "[INFO] Found ${#TEX_FILES[@]} file(s) matching ADictML*.tex"
fi

# Decide destination layout inside backup repo
STAMP="$(date +%Y%m%d_%H%M%S)"
if [[ "$BACKUP_LAYOUT" == "timestamp" ]]; then
  DEST="$BACKUP_DIR/snapshots/$STAMP"
  mkdir -p "$DEST"
  echo "[INFO] Timestamped backup destination: $DEST"
else
  DEST="$BACKUP_DIR"  # mirror into repo root
  echo "[INFO] Mirror backup destination: $DEST"
fi

backup_copy_one() {
  local src="$1"
  local dst_root="$2"
  local dst="$dst_root/$src"
  mkdir -p "$(dirname "$dst")"
  if [[ "$BACKUP_MODE" == "rsync" ]]; then
    rsync -a --delete-after "$src" "$dst"
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
  fi
  echo "  → Backed up: $src"
}

echo "[INFO] Backing up ADictML*.tex and extras ..."
for f in "${TEX_FILES[@]}"; do
  # TEX_FILES entries are relative like "./ADictML_English.tex" from find; normalize to no leading ./
  f="${f#./}"
  backup_copy_one "$f" "$DEST"
done

for f in "${EXTRAS_EXISTING[@]}"; do
  backup_copy_one "$f" "$DEST"
done

# Optionally delete old snapshots
if [[ "$BACKUP_LAYOUT" == "timestamp" ]]; then
  echo "[INFO] Pruning snapshots older than ${BACKUP_KEEP_DAYS} days ..."
  find "$BACKUP_DIR/snapshots" -mindepth 1 -maxdepth 1 -type d -mtime +"$BACKUP_KEEP_DAYS" -print -exec rm -rf {} \; || true
fi

# --- Commit & push inside the backup repo ---
echo "[INFO] Committing inside backup repository ..."
(
  cd "$BACKUP_DIR"
  git add -A
  git commit -m "Backup: $MSG" || echo "[INFO] No changes to commit in backup repo."
  git push
)

echo "[OK] Backup repo updated."