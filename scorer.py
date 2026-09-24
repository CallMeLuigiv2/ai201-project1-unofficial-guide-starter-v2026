# this file will be used to test our rag system
# must be fair normalize text
# must judge outputs
"""
scorer.py — decides whether one answer passed, and if not, why.

run_eval.py finds this file on its own and calls `judge` once per question per
run. It hands over four things and wants one bool back. That bool is
"pass" in the run log.

A bare bool can't say WHY something failed, so the real work is in `verdict`,
which returns a label. `judge` is just `verdict == "pass"`. The labels split a
failure by the pipeline stage it points at, which is what the diagnosis step
needs:

    pass              correct AND names a file it was actually given
    unsourced         correct, but names none of the retrieved files
    wrong-generation  the expected phrase WAS in a retrieved chunk, but the
                      answer doesn't contain it — the model had the fact
    wrong-retrieval   the expected phrase was in NONE of the retrieved chunks —
                      the model never had a chance
    refused           the relevance gate refused the question

Precedence when more than one applies: refused > wrong-retrieval >
wrong-generation > unsourced > pass. A wrong answer's sourcing is not reported.

"Fair" means both sides are normalized the same way before comparing:
lowercase, commas dropped inside numbers (40,000 == 40000), other punctuation
turned to spaces (25-minute == 25 minute), whitespace collapsed.

These labels are heuristics. "wrong-generation" means the phrase was in a
chunk and not in the answer; usually that is generation, but it can also be
the model saying the same fact in different words. The criteria in criteria.md
are still scored by reading the answers. The labels say where to look first.
"""

import re
import sys

from gate import REFUSAL


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"(?<=\d),(?=\d)", "", text)     # 40,000 -> 40000
    text = re.sub(r"[^a-z0-9\s]", " ", text)         # other punctuation -> space
    return re.sub(r"\s+", " ", text).strip()         # collapse whitespace


def _stems(results) -> set[str]:
    """Normalized filenames without extension: 'guide_marchwood.md' -> 'guide marchwood'."""
    return {_normalize(r.source.rsplit(".", 1)[0]) for r in results}


def _prose(answer: str, results) -> str:
    """The answer with its source citations removed, so a filename can't count
    as the fact. Otherwise 'meets at Brightwater (guide_marchwood.md)' would
    pass an expects of 'marchwood'."""
    text = _normalize(answer)
    for stem in _stems(results):
        if stem:
            text = text.replace(stem, " ")
    return text


def _correct(expects: str, answer: str, results) -> bool:
    return bool(expects.strip()) and _normalize(expects) in _prose(answer, results)


def _in_chunks(expects: str, results) -> bool:
    """Was the expected phrase available to the model at all?"""
    want = _normalize(expects)
    return bool(want) and any(want in _normalize(r.text) for r in results)


def _sourced(answer: str, results) -> bool:
    """Does the answer name a file it was actually given? A made-up filename
    does not count. Matches the stem so 'guide_marchwood' without '.md' passes."""
    text = _normalize(answer)
    return any(stem and stem in text for stem in _stems(results))


def verdict(question: str, expects: str, answer: str, results) -> str:
    """One label per answer. See the module docstring for what each means."""
    if REFUSAL.lower() in answer.lower():
        return "refused"
    if not _correct(expects, answer, results):
        return "wrong-generation" if _in_chunks(expects, results) else "wrong-retrieval"
    if not _sourced(answer, results):
        return "unsourced"
    return "pass"


def judge(question: str, expects: str, answer: str, results) -> bool:
    """What run_eval.py calls. True only for a full pass.

    Prints the label for anything that isn't a pass, so the reason scrolls by
    during the run instead of waiting to be read out of the results file.
    """
    label = verdict(question, expects, answer, results)
    if label != "pass":
        print(f"         [{label}]", file=sys.stderr, flush=True)
    return label == "pass"
