# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in week 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next week costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
One of my five questions asks what the farm shop in Corry Vale sells. The answer
only appears in two documents, guide_corry_vale.md and guide_eating.md. Retrieval
could get distracted, because nine of my guides have an "Eat and drink" section
that reads a lot like this one, guide_eating.md talks about food in every town,
and other places sell similar things (Elder Ness has a shop that sells basics,
Givens Mill and Kestrelford both sell bread). The system has to pick the one
chunk with the specific information out of all those similar ones. I expect this
question could be a miss, which is why my target is 4 of 5 and not 5 of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
The grounding instruction in generate.py explicitly tells the model to name the
file its answer came from, and the last line of the prompt repeats it. The
build_prompt function also puts "[from filename]" above every excerpt, so the
model only has to copy a filename that is already in front of it. The only way
this fails is if the model completely ignores an instruction it was given twice,
so I set the target at 5 of 5 and not 4 of 5. A refusal from the relevance gate
does not count as an answer here, because it never reaches the model.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
The five out-of-scope questions are about Mongolia, diesel engines, the World
Cup, ibuprofen and Rust. My corpus is 14 travel guides about one region, so none
of them should come back close to any chunk. I still allow one miss because I
have not measured my cutoff yet. 0.6 is the starter's default, and one question
could share general words with a guide and land under it. The ibuprofen question
is the one I would watch, since 10 of my 14 guides mention a hospital or a minor
injuries unit. That is why 4 of 5 and not 5 of 5. I will add the distances I
measured here after Milestone 4.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

For at least 9 of 10 sampled chunks (`python app.py chunks -n 10`), the chunk
holds exactly one whole `##` section of a guide: it starts at the section's
heading and ends at the end of the section's last sentence.

**Why this target:**
Every guide in my corpus is split into `##` sections, and each section is one
complete topic, like "Getting there" or "Eat and drink". A chunk that cuts through
a section cuts off the context of that paragraph. I measured the sections: there
are 84 of them, the longest is 711 characters and the median is 297, so every
section fits inside one chunk and nothing forces a chunker to cut one. The
starter's fixed 800-character chunker does badly at this: 41 of its 51 chunks mix
text from two or more sections, and only 18 of 51 end on a finished sentence. So
this target is not free. I allow 1 miss in 10 because every guide also has a
short intro above its first heading, and the shortest is just a 23-character
title, so an intro may have to be joined to the section after it.
Also chunks need to ensure that they hold the context of which area they are
referring too. without that the structure of what is being explained in each chunk will be oblivious to the model.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

In at least 14 of 15 answers (my five questions, three runs each), every number,
time and place name in the answer can be found in the document that the answer
names as its source.

**Why this target:**
I want every answer grounded in the documents, not in what the model already
knows, and criterion 2 only checks that a source is named, not that it is the
right one. I first wanted 98%, but with 15 answers the only possible scores are
15 of 15 (100%) or 14 of 15 (93%), so 14 of 15 is the closest target I can
actually measure. I did not pick 15 of 15 because the model is handed 5 chunks
from different guides and some of my facts appear in more than one (the Halden
Bay parking time is in three documents), so it could take a detail from one file
and name another. I did not go lower than 14 because the answers are only two or
three sentences and the instruction says to use only the documents, so there
are few facts per answer to get wrong. Anyone can check this with the run log
and a search of the named file.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     WEEK 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in week 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
