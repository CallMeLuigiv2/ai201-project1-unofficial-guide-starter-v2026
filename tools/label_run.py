#!/usr/bin/env python3
"""
Re-label every answer in a run log with scorer.py's current labels.

    python tools/label_run.py results/run_2026-09-23_1957_before.md
    python tools/label_run.py results/run_..._after.md --out results/labels_after.md

Why this exists: scorer.py gained the `hedged` label after the before run was
made. A fair before/after comparison needs both runs scored by the same
scorer, so this reads the answers back out of a run file and labels them
again. It spends no model calls.

Retrieval is re-run to get the chunks each answer was judged against (the
run file records only the source filenames). Whether that retrieval should be
week-1 semantic-only or week-2 hybrid is worked out from the run file's own
"Sources retrieved" lines, or forced with --mode.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import questions as qs  # noqa: E402
from scorer import verdict  # noqa: E402
from store import search  # noqa: E402

ENTRY = re.compile(
    r"### (.+?) — run (\d+)\n\n"
    r"- Best distance: ([\d.]+) \((passed|refused by) the gate\)\n"
    r"- Sources retrieved: (.*?)\n\n```\n(.*?)\n```",
    re.S,
)


def retrieve(question, top_k, hybrid):
    config.HYBRID_SEARCH = hybrid
    return search(question, top_k=top_k)


def detect_mode(entries, top_k):
    """Which retriever produced this run? The one whose sources match its log."""
    score = {False: 0, True: 0}
    for question in {e[0] for e in entries}:
        recorded = {s.strip() for s in next(e[4] for e in entries if e[0] == question).split(",")}
        for hybrid in (False, True):
            got = {r.source for r in retrieve(question, top_k, hybrid)}
            score[hybrid] += got == recorded
    return score[True] > score[False]


def main():
    ap = argparse.ArgumentParser(description="Label a run file with scorer.py's current labels.")
    ap.add_argument("run_file")
    ap.add_argument("--mode", choices=["auto", "semantic", "hybrid"], default="auto")
    ap.add_argument("--top-k", type=int, default=None)
    ap.add_argument("--out", help="also write the table to this file")
    args = ap.parse_args()

    text = Path(args.run_file).read_text(encoding="utf-8").replace("\r\n", "\n")
    entries = ENTRY.findall(text)
    if not entries:
        sys.exit(f"No answers found in {args.run_file}")

    top_k = args.top_k or config.TOP_K
    hybrid = {"semantic": False, "hybrid": True}.get(args.mode)
    if hybrid is None:
        hybrid = detect_mode(entries, top_k)
    mode = "hybrid" if hybrid else "semantic-only"

    expects = {q["question"].strip(): q["expects"] for q in qs.answered()}
    rows, counts = [], Counter()
    for question, run, distance, gate, sources, answer in entries:
        q = question.strip()
        label = verdict(q, expects.get(q, ""), answer, retrieve(q, top_k, hybrid))
        counts[label] += 1
        rows.append(f"| {q.replace('|', '/')} | {run} | {label} |")

    lines = [
        f"# Labels for `{Path(args.run_file).name}`",
        "",
        f"- Produced by: `tools/label_run.py` using `scorer.py::verdict`",
        f"- Retrieval re-run as: {mode}, top-k {top_k}",
        f"- Labels: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
        "",
        "| Question | Run | Label |",
        "|---|---|---|",
        *rows,
    ]
    out = "\n".join(lines)
    print(out)
    if args.out:
        Path(args.out).write_text(out + "\n", encoding="utf-8")
        print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
