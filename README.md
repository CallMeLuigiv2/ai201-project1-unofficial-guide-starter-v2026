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



**3.** (Week 2) Research, gaps, and ideas. After the before run I was stuck. Every criterion passed but the system still hedged on the railway question, and I didn't know what a real fix looked like or what production systems do about this. So I had Claude run deep research on production RAG (Anthropic's contextual retrieval post, RRF and hybrid search, cross-encoder reranking, RAGAS metrics, Hamel Husain's evals FAQ, a paper on RAG and reworded queries) and come back with options and numbers, not just names. Then I asked it to look for gaps in my system that I couldn't see. It tested five in-region questions the guides can't answer and found all five score under my 0.70 cutoff, so the gate can't stop them. It pointed out that none of my five criteria checks whether the answer actually answers the question, which is why the hedge passed everything. It also reworded my five test questions and the distances held, so wording wasn't my problem. From the options it suggested I picked hybrid search because it followed straight from my diagnosis, needed no install or re-index, and I already had a table predicting what it would do. Contextual retrieval, reranking, raising `TOP_K` and a no-hedging prompt all went into What's Still Broken with the reason each one wasn't picked.

**4.** (Week 2) Test runs and tooling. Claude wrote `scorer.py`'s labels from the design we agreed on, wrote `tools/label_run.py` and `tools/probe_unanswerable.py`, benchmarked retrieval on all ten questions before and after hybrid (and the off switch) before a single model call was spent, and then ran the after eval, the probe and the labelling for me. Things it got wrong or that broke, and what changed: the first scorer counted "meets at Brightwater (guide_marchwood.md)" as correct for `expects=marchwood` because the word was inside the filename, so it now strips citations before checking. It ran the starter's staff smoke test to check hybrid search and that overwrote my real index with fake embeddings; it rebuilt the index (same 94 chunks) and re-ran the test in a temp folder. That smoke test also caught hybrid returning chunks out of distance order, which is why the list is sorted nearest-first now. The probe crashed on the first try because the free tier allows 15 calls a minute, not the 30 the starter assumes, so it re-ran after the window. And the probe's one ANSWERED label was a false positive that I caught by reading the answer, not by trusting the tool. Every number in both run logs came from scripts it wrote, and I read all 30 answers myself.

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

**What I changed:** Hybrid search in `store.py::search`. Week 1 ranked chunks by meaning only (cosine distance). Now each chunk is also ranked by keywords (BM25) and the two rankings get fused by rank (RRF: add up `1/(60 + rank)` from each list, ranks not scores because the two scales don't mix). The top 5 by fused score come back. On purpose, each chunk keeps its cosine distance, the 5 still come back nearest first, and the nearest chunk is always one of the 5, so the gate sees the same number it did in week 1. All ten best distances are identical before and after, and the out of scope questions still get refused. Files touched: `store.py::search` (plus a BM25 cache and one line in `build_index` to clear it) and a `HYBRID_SEARCH` switch in `config.py`; `AI201_HYBRID=0` gives back the week 1 retriever. Chunker, index, cutoff, `TOP_K` and the prompt are untouched. `rank-bm25` was already installed.

Measurement changes, not system changes: `scorer.py` got a `hedged` label because the railway hedge had scored `pass`, `tools/label_run.py` re-labels a run with the current scorer (before run re-labeled in `results/labels_before.md`: hedged 1, pass 9, wrong-generation 5), and `tools/probe_unanswerable.py` asks five in-region questions the guides can't answer.

**Why I picked it:** The railway hedge was a retrieval problem. The chunk that literally says "Every railway line in the region meets here" ranked 6th by meaning with `TOP_K` at 5, so the model never saw it. It shares five exact words with the question (every, railway, line, region, meets): by keywords it's 1st, fused it's 2nd. I checked all five questions with `app.py retrieve` before spending a model call: the railway chunk now gets in and the other four stay at rank 1. `TOP_K = 6` would also pull it in, but that adds a sixth loose chunk to every prompt.

**How I got there:** After the before run I was stuck. Every criterion passed but the system still hedged, and I didn't know the right fix or what real systems do about this. So I had Claude run deep research on production RAG and bring back options. Hybrid search is basically the standard setup. Anthropic's contextual retrieval (a model writes a short context for each chunk before indexing) cuts retrieval failures by 49%, and 67% with a reranker, but it costs 94 model calls, a re-index, and changes the chunk text criterion 4 measures. Reranking is worth 5 to 15 points but needs the 2 GB sentence-transformers install. Query rewriting (HyDE) fixes wording mismatch, but Claude tested my five questions reworded and the distances held. A prompt that bans hedging got ruled out, the hedge was honest for what the model saw. The research also found two gaps I hadn't seen: my gate can't stop in-region questions the guides don't answer (five tested, all under 0.70), and none of my criteria checks whether the answer actually answers. Hybrid won because it follows straight from the diagnosis, needs no install or re-index, and I already had a table predicting what it should do. The rest went to What's Still Broken.

**What I expect, written before the run:** Criteria 1 to 5 stay MET with the same numbers. What should move is `hedged` on the railway question, 1 of 3 to 0 of 3; three runs can't prove a fix, only fail to contradict it. One build check exists (`results/hybrid_smoke_ask_after.md`): the "every railway line" chunk was in the prompt and the answer was "Every railway line in the region meets at Marchwood (guide_marchwood.md)", 18 output tokens vs 43 for the hedged one. Risk: lighthouse, Halden Bay and Brightwater got a different 4th or 5th chunk than before, so a new wrong-file citation on criterion 5 would come from that.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks hold exactly one whole `##` section | 9 of 10 | 9/10 | 9/10 | 9/10 | MET |
| 5. Every number, time and place name in the answer is in the named source | 14 of 15 | 5/5 | 5/5 | 5/5 | MET (15/15) |

Run file: `results/run_2026-09-27_2251_after.md`, produced by `run_eval.py::main`, hybrid search on, caching off, cutoff 0.70, top-k 5. Scored the same way as the before run: criterion 1 with `scorer.py::_in_chunks`, criteria 2 and 5 by script over all 15 answers, criterion 3 from the run file, criterion 4 unchanged because the chunker was not touched. Labels from `tools/label_run.py` are in `results/labels_after.md`: **pass 11, wrong-generation 4, hedged 0** (before: pass 9, wrong-generation 5, hedged 1).

The scorer's per-question table:

```
| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| what can be bought at a farm shop in cory vale | fail | pass | pass |
| how long is the walk in elder ness to the lighthouse  | fail | fail | fail |
| on summer weekends what time do halden bay lots tend to fill up  | pass | pass | pass |
| approximately how many people are in brightwater | pass | pass | pass |
| where does every railway line in the region meet at | pass | pass | pass |
```

The railway question, all three runs, from `generate.py::answer_from_chunks`. This is the question the improvement was for:

```
run 1:
Every railway line in the region meets at Marchwood (source: guide_marchwood.md).

run 2:
Every railway line in the region meets at Marchwood (source: guide_marchwood.md).

run 3:
According to `guide_marchwood.md`, every railway line in the region meets in Marchwood.
```

The gate, from `run_eval.py::check_out_of_scope`:

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.803 | refused |
| How do I change the oil in a diesel engine? | 0.888 | refused |
| Who won the 1994 World Cup? | 0.975 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.836 | refused |
```

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

Yes, on the one thing it was aimed at. Before, the railway question hedged in 1 of 3 runs. After, 0 of 3, and all three answers quote the sentence that actually answers it: "Every railway line in the region meets at Marchwood (source: guide_marchwood.md)". Before, even the two answers that didn't hedge only paraphrased the intro chunk ("the junction where everyone changes trains"), because the real sentence was never in the prompt. Now it is.

How I know it's the change and not luck: 0 of 3 after 1 of 3 could happen by chance about 30% of the time, so three runs can't prove it. What I can point at is the mechanism. The "every railway line" chunk was rank 6 before and is rank 4 now, so it's in the prompt, and all three answers use its exact wording. Also the one build check I did before the run (`results/hybrid_smoke_ask_after.md`) came out the same way.

The criteria table didn't move, and it shouldn't have. All five were MET before and the change doesn't touch the gate, the chunks or the sourcing. If the table had moved, something else changed too.

The risk I wrote down didn't happen. Lighthouse, Halden Bay and Brightwater got a different 4th or 5th chunk and no wrong-file citation showed up. Halden Bay now also cites `guide_regional_transport.md`, which really does say "Both Halden Bay lots fill by 10am on summer weekends", so that's an extra correct source, not an error.

The 4 wrong-generation labels are still the `expects` wording on the farm shop and lighthouse questions, same as before, and all of those answers are correct when you read them. The farm shop went fail/pass/fail to fail/pass/pass only because run 3 happened to say "Bread and cheese and little else" word for word. That's noise, not improvement, and I'm not counting it.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

Nothing is missed against my five criteria, before or after. That is not the same as nothing being broken.

**1. My criteria can't see a hedge.** The railway hedge in the before run passed all five criteria. The `hedged` label in `scorer.py` catches it now, but a label is not a criterion, and the target I'd want (0 hedges in 15 answers) was never written down before the results, so I can't claim it this unit. Next unit it becomes a criterion. I stopped here because adding a criterion after seeing results is the thing the brief says costs the point.

**2. The gate can't stop in-region questions the guides don't answer.** I ran five of them through the whole pipeline (`results/near_miss_probe_after.md`): a tram ticket price, a bakery opening time, a tour price, a taxi phone number, hotel room counts. All five scored between 0.26 and 0.43, well under the 0.70 cutoff, so the gate passed every one. The grounding prompt declined all five, so today it holds, but it's one layer with nothing behind it. The research explained why no cutoff fixes this: cosine distance can't tell "about what you asked" from "answers what you asked". What I'd try next is a check on the shape of the distances (the gap between rank 1 and rank 5) instead of the top-1 number, which the research found separates the two cases better than a fixed cutoff. I stopped because it would be a second system change.

**3. My probe tool mislabeled one of those five.** It said ANSWERED for the tram ticket, but the actual answer was "the exact price is not specified, but it costs less than two single fares", which is a decline. My hedge phrase list had "does not specify" but not "is not specified". I added it and confirmed it changes none of the 30 labels in the two runs. The probe file keeps its original label so the mistake stays visible.

**4. Two `expects` phrases are written too long** ("bread and cheese and little else", "25-minute walk"), so the scorer false-fails 7 of 30 correct answers across both runs. I didn't change them, that's moving the goalposts. Next unit they're one token each.

**5. Three runs is thin.** 1 of 3 to 0 of 3 is consistent with a fix, not proof of one. I'd run the railway question 10 times. I stopped because of quota: the free tier allows 15 calls a minute for this model, and the starter's `REQUESTS_PER_MINUTE` is 30, which is what crashed my probe the first time (the retry backoff tops out at 8 seconds and the service asked for 50). That's a starter setting, not mine, and I left it under the one-change rule.

**6. Options from the research I didn't take, and why.** Contextual retrieval (Anthropic: a model writes a short context for every chunk before indexing, 49% fewer retrieval failures, 67% with a reranker) would fix "meets here" directly, but it's 94 model calls, a re-index, and different chunk text for criterion 4. A cross-encoder reranker needs the 2 GB sentence-transformers install. Raising `TOP_K` adds a loose chunk to every prompt. Query rewriting (HyDE) didn't apply, my five questions reworded still retrieved fine. Metadata filtering, conversational memory and a second embedding model were last unit's stretch options and are out of scope now.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

**Criterion 1.** "The retrieved chunks include one that contains the answer" let the word Marchwood in an intro chunk count. I'd write: for 5 of 5 questions, the chunk containing the sentence that answers the question is retrieved. Under that version the railway question misses before (rank 6) and passes after (rank 4), and the improvement would have shown up in the criteria table instead of only in a scorer label.

**Criterion 3.** I'd swap two of the five out-of-scope questions for in-region questions the guides don't answer. Mongolia and Rust test the easy case. The tram ticket tests the gate that actually matters, and it would have shown me in week 1 that the gate can't do it.

**Criterion 5.** Criteria 2 and 5 both check sourcing and neither checks that the answer answers. I'd make 5 a correctness criterion: for 14 of 15 answers, the answer contains the `expects` phrase and does not decline any part of the question. That's the criterion the hedge would have failed.

**`expects`.** Write it as the shortest thing a right answer has to contain ("little else", "25"), not the corpus's own sentence. Two of my five cost me 7 false fails for nothing.
