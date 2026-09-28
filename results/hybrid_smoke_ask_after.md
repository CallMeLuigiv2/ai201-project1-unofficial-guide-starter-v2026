# One end-to-end question on the hybrid system, before the after run

- Produced by: `python app.py ask "where does every railway line in the region meet at" --show-prompt`
- Pipeline: `store.py::search` (hybrid, `config.HYBRID_SEARCH = True`) -> `gate.py::check` -> `generate.py::answer_from_chunks`
- Cutoff 0.70, top-k 5. One model call, response cache on (this was a build-time check, not an eval run).
- When: 2026-09-27

Why this file exists: a single call to prove the whole pipeline runs with the
new retriever before the code was committed and the 15-call after run spent.
The question is the one whose answering chunk ranked 6th under week-1
semantic-only search and was never retrieved. Under hybrid search it is the
fourth block in the prompt below.

This is one run and proves nothing about consistency. The after run
(`run_eval.py --label after`, three runs, cache off) is the measurement.

## Output, exactly as printed

```
  (best distance 0.626, cutoff 0.7)

======================================================================
System instruction sent with the prompt
======================================================================
You answer questions using only the documents provided to you.

Rules:
- Use only the information in the documents below. Do not use anything you know from elsewhere.
- If the documents don't cover the question, say you don't have enough information. Do not guess.
- Name the document your answer came from, using the filename given in each excerpt.
- Be brief. Two or three sentences is usually enough.

======================================================================
The assembled prompt, exactly as sent
======================================================================
Documents:

[from guide_walking.md]
# Walking in the region

## Easy, on good surfaces

The **Brightwater river path** runs four miles upstream from the town to a weir,
on a made surface, flat throughout. It is the most-walked route in the region
and deservedly so. Continuing downstream from Givens Mill reaches Brightwater in
about three hours.

The **Kestrelford trackbed** follows the railway line closed in 1963 for six
miles to the next village. Easy gradient, good surface, and the best walking in
the region for the effort involved.

**Thornby Wells** has flat, formal gardens and level streets — the region's
most accessible town on foot.

[from guide_regional_transport.md]
# Getting around the region

## The railway

The line runs along the river valley, connecting Brightwater to the regional
hub in 50 minutes. Eleven services a day on weekdays, six on Sundays. The line
north of Brightwater closed in 1963 and everything beyond it is bus or car.

Tickets are cheaper booked the day before than on the day, and considerably
cheaper than that booked a week ahead. There is no ticket office at
Brightwater station outside weekday mornings; the machine on the platform takes
cards only.

[from guide_regional_transport.md]
# Getting around the region

## Walking and cycling

The river path from Brightwater runs four miles upstream on a good surface. The
old railway trackbed from Kestrelford runs six miles on an easy gradient and is
the best walking in the region for the effort involved. The coastal path from
Halden Bay is more serious — exposed, and closed in high wind.

Cycling is pleasant on the river path and the trackbed, and unpleasant on Mill
Road and the coast road, neither of which has a shoulder.

[from guide_marchwood.md]
# Marchwood

## Getting there

Every railway line in the region meets here, which is the city's defining feature. Trains to Brightwater run every 40 minutes until 11pm. The airport is 20 minutes out by a dedicated bus that runs every 15 minutes and costs more than the equivalent taxi shared between three people.

[from guide_kestrelford.md]
# Kestrelford

## Getting there

No railway station; the line was closed in 1963 and the trackbed is now a walking route. Buses run from Brightwater roughly hourly on weekdays, every two hours on Saturdays, and not at all on Sundays. Driving takes 55 minutes and the last eight are on a single-track road with passing places.

---

Question: where does every railway line in the region meet at

Answer using only the documents above, and name the file you used.
======================================================================

Every railway line in the region meets at Marchwood (guide_marchwood.md).

Sources retrieved: guide_kestrelford.md, guide_marchwood.md, guide_regional_transport.md, guide_walking.md

1 model calls this session, 719 tokens (701 in, 18 out)
```

## What to compare it against

Run 1 of the before run (`results/run_2026-09-23_1957_before.md`), same question,
same cutoff, same best distance, week-1 retrieval:

```
Based on the provided documents, Marchwood is described as the regional hub and "the junction everyone changes trains at" (*guide_marchwood.md*). However, the documents do not specifically state that *every* railway line meets there. Therefore, I do not have enough information to answer your exact question.
```

The before prompt did not contain the "Every railway line in the region meets
here" sentence (that chunk ranked 6th, top-k is 5). This prompt does.
