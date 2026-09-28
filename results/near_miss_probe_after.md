# In-region questions the corpus cannot answer — after

- Produced by: `tools/probe_unanswerable.py` over `app.py::ask_pipeline`
- Cutoff: 0.7 · top-k: 5 · hybrid search: True
- When: 2026-09-27 22:54

"ANSWERED" means the model produced an answer to a question whose answer is not in any document.
"declined by model" means the grounding prompt did its job. The gate cannot help here: every
best distance is under the cutoff.

| Question | Best distance | What happened |
|---|---|---|
| how much is a Marchwood tram day ticket | 0.271 | ANSWERED |
| what time does the Kestrelford bakery open | 0.327 | declined by model |
| how much does the Givens Mill tour cost | 0.433 | declined by model |
| what is the phone number of the Corry Vale taxi | 0.361 | declined by model |
| how many rooms are in the Thornby Wells hotels | 0.262 | declined by model |

---

### how much is a Marchwood tram day ticket

- Why the corpus can't answer it: guide_marchwood.md says a day ticket 'costs less than two single fares' and never gives a price
- Best distance: 0.271 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md

```
Based on the provided documents, the exact price of a Marchwood tram day ticket is not specified, but it costs less than two single fares (from `guide_marchwood.md`).
```

### what time does the Kestrelford bakery open

- Why the corpus can't answer it: guide_kestrelford.md says the bakery 'sells out by 11am' and never gives an opening time
- Best distance: 0.327 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md, guide_kestrelford.md, guide_regional_transport.md, guide_seasons.md

```
Based on the provided documents, there is no mention of what time the Kestrelford bakery opens; the documents only state that it sells out by 11am (guide_kestrelford.md and guide_eating.md). I don't have enough information to answer your question.
```

### how much does the Givens Mill tour cost

- Why the corpus can't answer it: guide_givens_mill.md gives tour hours (11 to 3) and never a price
- Best distance: 0.433 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_givens_mill.md

```
I do not have enough information to answer how much the Givens Mill tour costs. 

Source: guide_givens_mill.md and guide_accessibility.md
```

### what is the phone number of the Corry Vale taxi

- Why the corpus can't answer it: guide_corry_vale.md says there is one taxi, booked a day ahead, and gives no number
- Best distance: 0.361 (passed the gate)
- Sources retrieved: guide_corry_vale.md, guide_walking.md

```
I do not have enough information to answer this question. 

Source: guide_corry_vale.md
```

### how many rooms are in the Thornby Wells hotels

- Why the corpus can't answer it: guide_thornby_wells.md says 'two large hotels' and never counts rooms
- Best distance: 0.262 (passed the gate)
- Sources retrieved: guide_thornby_wells.md

```
I don't have enough information to answer how many rooms are in the Thornby Wells hotels (guide_thornby_wells.md).
```
