#!/usr/bin/env bash
set -euo pipefail

# Build MOADT-complete.pdf from R-MOADT.md + 9 worked examples
# Requires: pandoc, xelatex (texlive-xetex)

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

OUTFILE="MOADT-complete.pdf"
COMBINED=$(mktemp /tmp/moadt-combined.XXXXXX.md)
trap 'rm -f "$COMBINED"' EXIT

# --- YAML metadata block ---
cat > "$COMBINED" << 'YAML'
---
title: "MOADT: Multi-Objective Admissible Decision Theory"
subtitle: "A formal decision theory for AI alignment"
author: "C. Matt Freeman, Ph.D. — mattf@globalmoo.com"
date: "2025"
documentclass: report
classoption:
  - 11pt
geometry: margin=1in
urlcolor: blue
linkcolor: blue
toccolor: black
mainfont: "TeX Gyre Pagella"
mathfont: "TeX Gyre Pagella Math"
monofont: "DejaVu Sans Mono"
header-includes:
  - \usepackage{longtable}
  - \usepackage{booktabs}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[L]{\leftmark}
  - \fancyhead[R]{\thepage}
  - \fancyfoot{}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \setlength{\parskip}{0.5em}
  - \setlength{\parindent}{0em}
---
YAML

# --- Main body: R-MOADT.md (skip header lines handled by YAML metadata) ---
# Skip lines 1-9: title, author, email, subtitle, separator
tail -n +10 R-MOADT.md >> "$COMBINED"

# --- Switch to appendix lettering ---
cat >> "$COMBINED" << 'TEX'

\appendix
\renewcommand{\chaptername}{Appendix}

TEX

# --- Append each worked example as an appendix chapter ---
for i in $(seq 1 9); do
    FILE="MOADT-worked-example-${i}.md"
    if [[ ! -f "$FILE" ]]; then
        echo "ERROR: $FILE not found" >&2
        exit 1
    fi

    echo "" >> "$COMBINED"
    # Each worked example starts with "# MOADT Worked Example N: Title"
    # Keep the # heading so pandoc makes it a \chapter (appendix-lettered)
    # Replace ✗ (U+2717) with LaTeX \texttimes since font lacks it
    sed 's/✗/×/g' "$FILE" >> "$COMBINED"
    echo "" >> "$COMBINED"

    # Add a page break between appendices (except after the last one)
    if [[ $i -lt 9 ]]; then
        echo '\newpage' >> "$COMBINED"
        echo "" >> "$COMBINED"
    fi
done

echo "Building $OUTFILE ..."

pandoc "$COMBINED" \
    -o "$OUTFILE" \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=2 \
    --highlight-style=tango \
    2>&1

if [[ -f "$OUTFILE" ]]; then
    PAGES=$(pdfinfo "$OUTFILE" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
    SIZE=$(du -h "$OUTFILE" | cut -f1)
    echo "Success: $OUTFILE ($PAGES pages, $SIZE)"
else
    echo "ERROR: $OUTFILE was not created" >&2
    exit 1
fi
