# The Unofficial Guide

Name: Stanluigi Saint-Ruste
Corpus: city_guides

---

# Week 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

So for this project i chose the city_guides corpus which contains information about areas and the conviences one could find while there. it is 14 travel guides for a fictional region that covers roughly nine towns. the other five guides peratin to eating, walking, transport, seasons and accessibility. Each guide has sections within them that help categorize things for lookup. for example like "Getting there", "Eat and drink", " Where to stay" etc.. . So questions like "How long is the walk to the Elder Ness lighthouse" can be answerd from retrieved documents and names the file  it came from for further confirmation. however, if a question is not within the guides their are gates within the system that refuses to answer the question instead of giving an outright guess.

## Chunking Strategy

**Chunk size:** Flexible. Each chunk is one `##` section with the document title on top, so the document sets the size. Sections run from 176 to 711 characters, with a median of 297 characters, so we can afford to use this method.

**Overlap:** 0. This is handled because each `##` subheading carries its own context, so each chunk has its own topic and there are no cutoffs.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

One thing I noticed is that in the city_guides corpus, there is a heading that applies to the overall document and a subheading that applies to each specific paragraph. So each chunk includes the heading of the document for context, and the corresponding subheading for that paragraph. This is effective because we do not have to concern ourselves much with overlap. The reason is that each subheading holds its own topic within the document. Overlap is only needed when a sentence has the potential of being cut off, but in our case that should not happen if each chunk contains one subheading and the overall document heading.

Some documents go heading -> paragraph -> subheading -> paragraph -> subheading -> paragraph, and so on. Others go heading -> subheading -> paragraph -> subheading -> paragraph. The chunker handles the first case: the intro paragraph becomes its own chunk, and a title with nothing under it is skipped.

Our config.py has a defined CHUNK_SIZE and CHUNK_OVERLAP, but these do not apply to our chunking mechanism. They are only used when the starter's fallback chunker is called instead.

**Results from my chunker** (`chunker.py::split_documents`):

- 94 chunks
- 322 characters on average
- 174 shortest
- 762 longest
- Every chunk ends on a finished sentence, with no mixing of two sections

**Starter chunker** (`chunker.py::fallback_split`):

- 51 chunks
- Shortest 24 characters
- 41 of 51 chunks have a mixture of two or more sections

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

Note: Chunk 1 is an intro chunk, the text above a guide's first `##` heading. It is the weakest kind of chunk my chunker makes, because it cannot answer a question on its own. I kept intro chunks anyway because some of them hold real answers: the intro of `guide_brightwater.md` is the only place in the corpus that gives the town's population (about 40,000), which is one of my test questions.

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** where does every railway line in the region meet at

**Answer:** (from `python app.py ask`, one model call)

```
  (best distance 0.626, cutoff 0.7)

Based on the provided documents, Marchwood is described as "the regional hub — 180,000 people, the junction everyone changes trains at." (Source: guide_marchwood.md)

Sources retrieved: guide_marchwood.md, guide_regional_transport.md, guide_walking.md

1 model calls this session, 719 tokens (676 in, 43 out)
```

This is the question the starter's default cutoff of 0.6 would have refused (best distance 0.626). At 0.70 it passes the gate, the answer names its source in the text, and the fact it quotes is in `guide_marchwood.md`.

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

0.70, set in config.py.

I ran the five test questions and the five out-of-scope questions, and wrote down the best distance for each. The two groups showed no overlap. The five in-corpus questions scored between 0.214 and 0.626, while the five out-of-scope questions scored between 0.803 and 0.975, meaning the gap is 0.626 to 0.803, so the cutoff belongs in that range. That is why the starter cutoff had to be adjusted from its default 0.6 to 0.70. The reason for this adjustment is that one of the questions (the railway one in particular) scored 0.626, so with the default at 0.6 the gate refused it even though the answer is within the retrieved chunks. I picked 0.70 rather than the middle of the gap because it leans toward refusing, and a wrong refusal is cheaper than handing the model weak chunks.

What I would get wrong at 0.70: after some more testing, a rephrased version of the railway question ("which city do all the railway lines meet at") scored 0.60, showing me that a different wording of the same question can still get refused. In the other direction, the gate only catches questions from another world. A question about my region that the corpus does not answer, like the price of a Marchwood tram ticket, would score well under 0.70 and get through, and only the grounding prompt in generate.py can stop that.

| Question | In corpus? | Best distance |
|---|---|---|
| what can be bought at a farm shop in cory vale | yes | 0.495 |
| how long is the walk in elder ness to the lighthouse | yes | 0.244 |
| on summer weekends what time do halden bay lots tend to fill up | yes | 0.288 |
| approximately how many people are in brightwater | yes | 0.214 |
| where does every railway line in the region meet at | yes | 0.626 |
| What is the capital of Mongolia? | no | 0.803 |
| How do I change the oil in a diesel engine? | no | 0.888 |
| Who won the 1994 World Cup? | no | 0.975 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.835 |
| How do I write a for loop in Rust? | no | 0.837 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I asked claude to basically help me with understanding the gaps for a proper baseline cutoff, syntax issues when explaining things for the criteria and readme.so i can properly convey my thoughts and ideas. moving things for formating etc...

To give an example i wrote a reason for criterion 1  around a "small market in cory vale" that only appeared one document. i asked claude whether it was the kind of answer the rubric wanted. it checked the corpus and came back with problems that my writings had. cory vale had no markets, it had a farm shop. the word market is repeated multiple times within the documents, this would affect the model from retrieving the correct chunks. So after revision i edited my question and changed my expected to match. 



**2.**
 I wrote the plan for my chunker in the README first (one ## section per chunk, document title on top, intro paragraph as its own chunk, bare titles skipped, overlap 0) and asked Claude to write split_documents from those notes. The first version it wrote crashed with a SyntaxError, because the \n inside two string literals had been written into the file as real line breaks, and it had to be repaired. Before trusting it I predicted the chunk count from my measurements (84 sections + 10 intros = 94) and the function produced exactly 94. I also had it walk me through the regex and answered three questions about it, including what happens to a corpus with no ## headings at all. I kept my design rather than trying a fancier chunker; there's probably a better method, but this one was mine and the results held up.



<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks hold exactly one whole `##` section | 9 of 10 | 9/10 | 9/10 | 9/10 | MET |
| 5. Every number, time and place name in the answer is in the named source | 14 of 15 | 5/5 | 5/5 | 5/5 | MET (15/15) |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Run file: `results/run_2026-09-23_1957_before.md`, produced by `run_eval.py::main` with caching off, cutoff 0.70, top-k 5.

The per-question table `run_eval.py` wrote, scored by `scorer.py::judge`:

```
| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| what can be bought at a farm shop in cory vale | fail | pass | fail |
| how long is the walk in elder ness to the lighthouse  | fail | fail | fail |
| on summer weekends what time do halden bay lots tend to fill up  | pass | pass | pass |
| approximately how many people are in brightwater | pass | pass | pass |
| where does every railway line in the region meet at | pass | pass | pass |
```

That table shows 10 pass / 5 fail. All five fails are the `expects` wording, not the system, and all five answers behind them are correct. See Diagnoses.

**Criterion 1** — retrieval is deterministic, so this is one check per question: is the `expects` phrase in any of the five chunks `store.py::search` returns? Checked with `scorer.py::_in_chunks`:

```
yes  expects='bread and cheese and little else' found in guide_eating.md#4
yes  expects='25-minute walk'                   found in guide_elder_ness.md#2
yes  expects='10am'                             found in guide_seasons.md#1, guide_halden_bay.md#1
yes  expects='40,000'                           found in guide_brightwater.md#0
yes  expects='marchwood'                        found in guide_marchwood.md#0, guide_marchwood.md#2
```

**Criteria 2 and 5** — the five answers from run 1, exactly as `generate.py::answer_from_chunks` returned them. Every one names a file that was retrieved (criterion 2), and every number, time and place in them is in the file it names (criterion 5):

```
Q: what can be bought at a farm shop in cory vale
best distance 0.4953, sources retrieved: guide_corry_vale.md, guide_eating.md

Based on the provided documents, the farm shop at the valley mouth sells bread, cheese, and little else. 

Source: `guide_corry_vale.md` (also mentioned in `guide_eating.md`)

Q: how long is the walk in elder ness to the lighthouse
best distance 0.2445, sources retrieved: guide_elder_ness.md, guide_walking.md

The walk to the lighthouse in Elder Ness is 25 minutes. 

Source: `guide_elder_ness.md` and `guide_walking.md`

Q: on summer weekends what time do halden bay lots tend to fill up
best distance 0.2881, sources retrieved: guide_halden_bay.md, guide_seasons.md

On summer weekends, parking lots in the town fill up by 10am (guide_halden_bay.md).

Q: approximately how many people are in brightwater
best distance 0.2137, sources retrieved: guide_brightwater.md, guide_marchwood.md, guide_regional_transport.md, guide_thornby_wells.md

Brightwater has a population of about 40,000 people, which roughly doubles during term time (guide_brightwater.md).

Q: where does every railway line in the region meet at
best distance 0.6264, sources retrieved: guide_marchwood.md, guide_regional_transport.md, guide_walking.md

Based on the provided documents, Marchwood is described as the regional hub and "the junction everyone changes trains at" (*guide_marchwood.md*). However, the documents do not specifically state that *every* railway line meets there. Therefore, I do not have enough information to answer your exact question.
```

**Criterion 3** — `run_eval.py::check_out_of_scope`, one deterministic pass:

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.803 | refused |
| How do I change the oil in a diesel engine? | 0.888 | refused |
| Who won the 1994 World Cup? | 0.975 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.836 | refused |
```

**Criterion 4** — not touched by `run_eval.py`. Evidence is `results/criterion4_chunks_sample.txt`, the output of `python app.py chunks -n 10` on `chunker.py::split_documents`. Nine of the ten chunks are exactly one `##` section with the document title on top. The one miss is Chunk 1, an intro chunk:

```
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

A passing one, for comparison:

```
Chunk 2  |  source: guide_brightwater.md#4  |  produced by: chunker.py::split_documents
# Brightwater

## What to see

The mill building itself is now a museum and is genuinely good, particularly the section on what happened to the town after it closed. Allow 90 minutes. The river walk runs four miles upstream to a weir and is the thing most people remember. The cathedral is small and 14th century and takes 20 minutes.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | 5 of 5 against a 4 of 5 target, in all three runs. Retrieval does not change between runs, so I checked once whether the `expects` phrase appears in any of the five retrieved chunks, and it does for every question. The close call is the railway question: the chunk with the literal sentence "Every railway line in the region meets here" ranks 6th and was not retrieved. But the answer, Marchwood, is in the retrieved intro chunk ("Marchwood is the regional hub... the junction everyone changes trains at"), and the criterion asks whether a retrieved chunk contains the answer, not whether it contains the best sentence. |
| 2 | Every answer names a source | MET | 15 of 15 answers name a file, and in every case it is a file that was actually retrieved. None made a filename up. The target was 5 of 5 and it held in every run. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 refused. Best distances were 0.803 to 0.975, all above the 0.70 cutoff, with the closest one (Mongolia, 0.803) still 0.10 over. This is one deterministic pass, so the same number is in all three columns. |
| 4 | Sampled chunks hold exactly one whole `##` section | MET | 9 of 10 against a 9 of 10 target. The one miss is the accessibility guide's intro chunk, which has no `##` heading. My reason for the target said an intro chunk could land in the sample, and it did. |
| 5 | Every number, time and place name in the answer is in the named source | MET | 15 of 15 against 14 of 15. I checked every number and time in all 15 answers against the cited file by script, and every place name by reading. The lighthouse answers cite two files; both `guide_elder_ness.md` and `guide_walking.md` say the walk is 25 minutes, so that is a correct double attribution. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I missed nothing. All five criteria came out MET on the first run, and the numbers did not move between runs. However, their are much more improvements that could be made, like better senetence structures. Making sure to handle the parsing cases for these situations 

"Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
# Getting around the region with limited mobility"

My chunker needs to be more dynamic and diverse for edge cases.



### Were my targets set low?

Partly no. Criterion 1's 4 of 5 came from a real prediction (the farm shop question) that turned out wrong in the other direction. Criterion 3's cutoff was measured against a real gap. Criterion 4's 9 of 10 is a target the starter's chunker fails badly (41 of 51 chunks mixed sections). Those were not safe numbers.

But there is a hole, and the run found it. None of my five criteria measures whether the answer actually answers the question. Criterion 2 checks that a source is named, criterion 5 checks that the facts are in that source, and criterion 1 checks that the fact was retrievable. An answer can do all three and still decline. Run 1 of the railway question did exactly that:

```
Based on the provided documents, Marchwood is described as the regional hub and "the junction everyone changes trains at" (*guide_marchwood.md*). However, the documents do not specifically state that *every* railway line meets there. Therefore, I do not have enough information to answer your exact question.
```

That answer names its source, quotes a sentence that is really in the file, and the retrieved chunks do contain "Marchwood". It passes all five criteria. It also does not answer the question. Runs 2 and 3 answered the same question plainly from the same chunks, so this is a hedge the model makes some of the time, but not every time, and my criteria does not address that.

### Diagnosis of the hedge: retrieval, with generation on top

**Stage: retrieval.** The sentence that answers the question outright, "Every railway line in the region meets here", is in `guide_marchwood.md` under `## Getting there`. That chunk ranks 6th at distance 0.710, and `TOP_K` is 5, so the model never saw it. It saw the Marchwood intro chunk (rank 2), which says "regional hub" and "junction everyone changes trains at" but never says "every line".

**Mechanism.** The answer to this question is the name of the town, and my chunker puts the town name in the title line at the top of each chunk. The body of the `Getting there` section says "meets **here**", not "meets at Marchwood", and the rest of that section is about airport buses and train frequencies, which pulls the embedding away from the question. So the chunk that contains the exact sentence looks less like the question than four other chunks that only share words like "railway" and "region". In week 1 I wrote down that this chunk sat at rank 6 and that I would keep `TOP_K` at 5 unless it caused a miss. It caused a hedge in one run of three.

**Generation on top.** Given the same five chunks, the model answered plainly twice and hedged once. That variance is generation, but it is variance on a thin input. With the "every line" sentence in the prompt there would be nothing to hedge about.

### Two measurement problems, not system problems

**1. The scorer fails correct answers on two questions.** Five of the fifteen scorer verdicts are `fail`, and all five are false. The farm shop `expects` is "bread and cheese and little else" and the model writes "bread, cheese, and little else"; the lighthouse `expects` is "25-minute walk" and the model writes "is 25 minutes". Both `expects` phrases were written as exact corpus wording instead of the one token a correct answer must contain ("little else", "25"). The stage is not in the pipeline at all; it is the test. I have not changed those `expects` values, because changing them after seeing results would be moving the goalposts. The rows above are judged by reading.

**2. The scorer's refusal check missed the hedge.** `scorer.py` labels an answer `refused` only if it contains the gate's exact refusal string. The railway hedge says "I do not have enough information to answer your exact question", which is different wording, so the scorer labeled it `pass`. A soft refusal written by the model looks nothing like the hard refusal written by the gate.

### The pattern

Both real findings are the same question, and it is the one question whose answer is the name of the document rather than a fact inside a section. For the other four questions, the answer sits in the body of the section ("25-minute walk", "fill by 10am", "about 40,000", "little else"). For the railway question, the body says "here" and only the title says where. Section-based chunks with a title line on top are strong when the fact is in the body and weak when the fact is the title.

### What I would tighten, and to what

Criterion 1. As written it asks whether a retrieved chunk contains the answer, and "Marchwood" in an intro chunk satisfies it. I would tighten it to: for all 5 of 5 questions, the chunk containing the sentence that answers the question is among the retrieved chunks. Under that version the railway question misses (rank 6), and the run log would have shown the retrieval gap directly instead of it surfacing as a hedge in one run out of three.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
