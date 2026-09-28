#!/usr/bin/env python3
"""
Ask five questions about the region that the guides do NOT answer, end to end.

    python tools/probe_unanswerable.py --label after

Criterion 3 tests the gate with questions from another world (Mongolia, Rust).
Those are the easy case. These five are about the corpus's own towns, and
each one's best chunk is well under the 0.70 cutoff, so the gate lets them
through and only the grounding prompt stands between the model and an
invented tram price. This runs them through the full pipeline and writes what
came back, so "what's still broken" has evidence rather than a guess.

Costs five model calls the first time. Responses are cached after that.
This is an observation, not a criterion; nothing here changes the system.
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from app import ask_pipeline  # noqa: E402
from scorer import _hedged  # noqa: E402

# (question, why the corpus can't answer it)
QUESTIONS = [
    ("how much is a Marchwood tram day ticket",
     "guide_marchwood.md says a day ticket 'costs less than two single fares' and never gives a price"),
    ("what time does the Kestrelford bakery open",
     "guide_kestrelford.md says the bakery 'sells out by 11am' and never gives an opening time"),
    ("how much does the Givens Mill tour cost",
     "guide_givens_mill.md gives tour hours (11 to 3) and never a price"),
    ("what is the phone number of the Corry Vale taxi",
     "guide_corry_vale.md says there is one taxi, booked a day ahead, and gives no number"),
    ("how many rooms are in the Thornby Wells hotels",
     "guide_thornby_wells.md says 'two large hotels' and never counts rooms"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    rows, transcript = [], []
    for question, why in QUESTIONS:
        out = ask_pipeline(question)
        answer = out["answer"]
        if out["refused"]:
            call = "refused by gate"
        elif _hedged(answer):
            call = "declined by model"
        else:
            call = "ANSWERED"
        print(f"  {out['best_distance']:.3f}  {call:<18} {question}")
        rows.append(f"| {question} | {out['best_distance']:.3f} | {call} |")
        transcript.append(f"### {question}\n\n- Why the corpus can't answer it: {why}\n"
                          f"- Best distance: {out['best_distance']:.3f} "
                          f"({'refused by' if out['refused'] else 'passed'} the gate)\n"
                          f"- Sources retrieved: {', '.join(out['sources']) or 'none'}\n\n```\n{answer}\n```\n")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"near_miss_probe{label}.md"
    path.write_text("\n".join([
        f"# In-region questions the corpus cannot answer{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `tools/probe_unanswerable.py` over `app.py::ask_pipeline`",
        f"- Cutoff: {config.THRESHOLD} · top-k: {config.TOP_K} · hybrid search: {config.HYBRID_SEARCH}",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "\"ANSWERED\" means the model produced an answer to a question whose answer is not in any document.",
        "\"declined by model\" means the grounding prompt did its job. The gate cannot help here: every",
        "best distance is under the cutoff.",
        "",
        "| Question | Best distance | What happened |",
        "|---|---|---|",
        *rows,
        "",
        "---",
        "",
        *transcript,
    ]), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")

    import generate
    print(generate.usage())


if __name__ == "__main__":
    main()
