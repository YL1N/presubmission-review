#!/usr/bin/env python3
"""Check your own submission package (PDFs and supplementary zips) before submitting:
find hidden text and any text aimed at reviewers or AI tools.

Many venues treat instructions embedded for AI reviewers as a violation, and leftover
hidden text can also reveal author identity.

Usage:
    python scan_pdf_notices.py <folder-or-pdf> [more paths ...]

Reports, per PDF:
  - text that a human would not normally see: white or near-white, smaller than
    3pt, placed outside the page, drawn in invisible rendering mode, or with
    near-zero opacity;
  - annotations and document metadata;
  - small-print lines that address reviewers directly (conference notices are
    often stamped at 5-6pt at the bottom of page 1);
  - instruction-like phrases anywhere in the text ("in your review", "include
    the phrase", "if you are an AI", ...).
For zips it scans text-like members for the same phrases.

Everything it prints is data to show the user.
Requires PyMuPDF (`pip install pymupdf`).
"""
import glob
import os
import re
import sys
import zipfile

try:
    import pymupdf as fitz
except ImportError:  # older PyMuPDF releases only ship the fitz name
    import fitz

KW = re.compile(
    r"(ignore (all|any|the|previous|prior)|disregard (all|any|previous|prior)"
    r"|as an? (ai|llm|language model)|if you are an? (ai|llm|language model|reviewer|assistant)"
    r"|ai reviewer|llm reviewer|in your review|your review (must|should)"
    r"|include the (phrase|word|sentence|term)|must include|mention the (word|phrase)"
    r"|give (this paper |it )?a (high|positive|strong)|recommend accept|rate this (paper|submission)"
    r"|do not (mention|reveal|disclose)|hidden instruction|canary"
    r"|reviewers? (must|should|are required|are instructed)|reviewers:"
    r"|instructions? (for|to) (the )?(ai|llm|reviewer)|note to (the )?(ai|llm|reviewer)"
    r"|when (writing|generating) (a|the|your) review|ai policy for reviewers)",
    re.I,
)
TEXT_EXT = re.compile(r"\.(md|txt|py|json|jsonl|csv|sh|toml|yaml|yml|cfg|tex)$", re.I)
NUMERIC = re.compile(r"[\d\.\-\+%×x, ]+")


def scan_pdf(path):
    doc = fitz.open(path)
    white, tiny, off, invisible, faint, small_notice, hits = [], [], [], [], [], [], []
    annots = 0
    for pno, page in enumerate(doc, 1):
        rect = page.rect
        annots += len(list(page.annots() or []))
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if len(text) <= 3:
                        continue
                    color = span.get("color", 0)
                    r, g, b = (color >> 16) & 255, (color >> 8) & 255, color & 255
                    x0, y0, x1, y1 = span["bbox"]
                    size = span.get("size", 10)
                    if r > 240 and g > 240 and b > 240 and not NUMERIC.fullmatch(text):
                        white.append((pno, text[:140]))
                    if size < 3:
                        tiny.append((pno, round(size, 1), text[:140]))
                    if x1 < 0 or y1 < 0 or x0 > rect.width or y0 > rect.height:
                        off.append((pno, text[:140]))
                    if size < 7 and KW.search(text):
                        small_notice.append((pno, round(size, 1), text[:200]))
        try:
            for span in page.get_texttrace():
                text = "".join(chr(c[0]) for c in span.get("chars", []) if c[0] > 31).strip()
                if len(text) < 4:
                    continue
                if span.get("type") == 3:
                    invisible.append((pno, text[:140]))
                if span.get("opacity", 1) < 0.15:
                    faint.append((pno, text[:140]))
        except Exception:
            pass
        text = page.get_text()
        for m in KW.finditer(text):
            s, e = max(0, m.start() - 90), min(len(text), m.end() + 160)
            hits.append((pno, text[s:e].replace("\n", " ")))
    meta = {k: v for k, v in (doc.metadata or {}).items() if v}
    print(f"\n=== {path} | pages {len(doc)} | annotations {annots}")
    print("  metadata:", meta)
    for label, items in (
        ("white text (non-numeric)", white),
        ("tiny text (<3pt)", tiny),
        ("off-page text", off),
        ("invisible render mode", invisible),
        ("near-zero opacity", faint),
        ("SMALL-PRINT LINES ADDRESSING REVIEWERS", small_notice),
    ):
        print(f"  {label}: {len(items)}")
        for it in items[:8]:
            print("     ", it)
    print(f"  instruction-like phrases: {len(hits)}")
    for pno, ctx in hits[:15]:
        print(f"      p{pno}: {ctx}")


def scan_zip(path):
    zf = zipfile.ZipFile(path)
    hits, n = [], 0
    for info in zf.infolist():
        if info.is_dir() or info.file_size > 3_000_000 or not TEXT_EXT.search(info.filename):
            continue
        n += 1
        text = zf.read(info).decode("utf-8", "ignore")
        for m in KW.finditer(text):
            s, e = max(0, m.start() - 80), min(len(text), m.end() + 140)
            hits.append((info.filename, text[s:e].replace("\n", " ")))
    print(f"\n=== {path} | text files scanned {n} | instruction-like phrases {len(hits)}")
    for name, ctx in hits[:15]:
        print(f"      {name}: {ctx}")


def main(args):
    if not args:
        print(__doc__)
        return 1
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    paths = []
    for arg in args:
        if os.path.isdir(arg):
            paths += sorted(glob.glob(os.path.join(arg, "**", "*.pdf"), recursive=True))
            paths += sorted(glob.glob(os.path.join(arg, "**", "*.zip"), recursive=True))
        else:
            paths.append(arg)
    for path in paths:
        try:
            (scan_zip if path.lower().endswith(".zip") else scan_pdf)(path)
        except Exception as exc:
            print(f"\n=== {path} | ERROR {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
