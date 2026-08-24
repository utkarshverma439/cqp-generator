# Engineering Assignment — Dynamic Cell Qualification Protocol Generator

**Role:** Senior / Staff Software Engineer (Document Automation)
**Time window:** **48 hours** from the moment this pack is sent to you. Submit whatever you have at the deadline.
**Expected investment:** This is deliberately larger than a day's work. We are not looking for "finished" — we are looking for how far a strong engineer gets, and *which* parts they get right.

---

## 1. The product, in one paragraph

Northgate Cell Qualification Laboratory (NCQL) qualifies rechargeable battery cells against a regulatory framework called **IESF‑4400**. For every cell they test, an engineer today hand-assembles a **Cell Qualification Protocol (CQP)** — a formal Word document — by copying numbers and tables out of three source documents into a fixed template. It is slow, error-prone, and does not scale. Your job is to **replace that human** with software.

You will build a service that ingests the three source documents for *any* cell and emits the finished, correctly-formatted **CQP `.docx`** — with no manual touch-up. A reviewer should be able to open your output, sign it, and issue it.

Read **`02_Domain_Primer.md`** before you start — it explains the domain in plain language. You do **not** need any battery or regulatory background beyond that primer.

---

## 2. What you are given

```
candidate_pack/
├── 02_Domain_Primer.md                  ← read this first
├── 03_CQP_Field_and_Token_Reference.md  ← every template token and where its value comes from
├── 04_Frontend_Requirements.md          ← the minimal UI you must ship
├── template/
│   └── CQP_Template.docx                ← the protocol template you must fill (DO NOT restructure it)
├── reference_example/
│   └── CQP_SetA_GOLD.docx               ← the EXACT output your tool must produce for Set A
└── inputs/
    ├── setA/   TMP_*.docx   ACL_*.docx   DATASHEET_*.pdf     ← worked example (gold provided)
    ├── setB/   TMP_*.docx   ACL_*.docx   DATASHEET_*.pdf     ← held-out, you produce the output
    └── setC/   TMP_*.docx   ACL_*.docx   DATASHEET_*.pdf     ← held-out, harder
```

The three source documents per cell are:

| File | What it is | Format |
|---|---|---|
| `TMP_*.docx` | **Test Method Procedure** — the methods/SOP for the qualification tests | Word |
| `ACL_*.docx` | **Acceptance Criteria & Limits** — the pass/fail limits, organised by *duty profile* | Word |
| `DATASHEET_*.pdf` | The cell vendor's **product datasheet** — electrical ratings, discharge curve, capacity grading | PDF |

**Set A is fully worked for you:** we ship the three inputs *and* `CQP_SetA_GOLD.docx`, the exact document your tool must generate from them. Treat it as the specification of "correct." Sets **B** and **C** ship inputs only — your tool must generate their protocols too, and we will compare what you produce against our held-out gold copies.

---

## 3. What you must build

1. **A generator** that takes `(TMP.docx, ACL.docx, DATASHEET.pdf)` for one cell and writes a filled `CQP_<cell>.docx`.
2. **A basic web frontend**: upload the three files, click *Generate*, download the resulting `.docx`. Nothing fancy — a single page is fine. It exists so we can run your tool without reading your code.
3. **A short `SOLUTION.md`**: how to run it, your architecture, what you got working, what you didn't, and — importantly — **the assumptions you made and where you think your tool would break.**

Stack is your choice. It must run on a clean machine from your README in under ten minutes.

---

## 4. The hard requirement: it must be *dynamic*

A tool that only works on Set A is worth almost nothing to us. The whole point is that NCQL onboards new cells constantly, each with a different shape:

- **Different numbers of duty profiles.** Set A has two. Set B has one. Set C has three. Your tool must not assume a fixed count, and the template's *Duty Profile Test Matrix* (Table 1) and *Section 7* blocks must expand to match — exactly as the gold for Set A shows.
- **Different test lists and limits per duty profile.** The same cell can carry different acceptance limits for, say, "Automotive Traction" vs "Grid Storage." The Section 7 table for each profile must reflect *that profile's* rows from the ACL.
- **Different source-document wording.** The three sample sets do not use identical headings or phrasing in their TMP/ACL files. The same logical section may be titled differently across cells. Do not hard-code to the literal strings you see in Set A.
- **Numbers that differ per cell** and that come from the datasheet, not from anywhere you can type them in.

We are explicitly telling you: **the obvious 80%-solution will pass Set A and fail Sets B and C.** Getting B and C right is most of the signal.

---

## 5. Correctness bar (how we grade output)

For each set, we diff your generated `.docx` against our gold along these axes. **Exact** means character-for-character in the relevant cell/paragraph.

1. **Every field is populated** — no `{{ token }}` may survive into the output, anywhere (body, tables, headers/footers).
2. **Numeric values are exact.** The cell's nominal/charge/discharge voltages, rated capacity, and graded-capacity band must match the cell's actual datasheet values. Wrong or blank numbers here are an automatic fail for that set, regardless of formatting. *(These specific numbers are the single most common reason a submission fails. Budget for them.)*
3. **The Duty Profile Test Matrix (Table 1)** has exactly one row per (duty profile × conditioning rate), correctly numbered, with the duty-profile cell merged across its rate rows — see the gold.
4. **Each Section 7 block** lists exactly the tests for its duty profile, renumbered `1..n`, with the acceptance limits and any limit markers carried verbatim from the ACL.
5. **Footnotes/notes** referenced by markers in the ACL appear, verbatim, where the template calls for them.
6. **Formatting is preserved** — fonts, shading, borders, the header/footer, table column widths. The output should be visually indistinguishable from the gold to a reviewer.
7. **Nothing is invented and nothing bleeds.** Sections that are meant to stay blank at issue stay blank. Data for one duty profile does not leak into another's table, and source data does not leak into places it does not belong.
8. **The issued protocol is locked for review**, with only the per-profile *Acceptance Criteria* and *Conclusion* blocks left editable — matching the gold's behaviour when opened in Word.

We will open every output in **Microsoft Word**, not only your renderer. "It looks right in LibreOffice / my viewer" is not sufficient; malformed documents that Word repairs on open are penalised.

---

## 6. Constraints

- **Do not edit the template's structure, styles, or wording.** You fill it; you do not rebuild it. (You may, of course, clone its rows/blocks as needed.)
- **Do not transcribe Set A's gold values into your code.** We will run Sets B and C, and we read submissions. Hard-coded answers are an immediate disqualification.
- No paid third-party services are required to complete this. If you choose to use any external API, it must be runnable by us with a key we can supply, and your tool must degrade gracefully without it. Document every dependency.
- Keep secrets out of the repo.

---

## 7. What we are really evaluating

- **Faithfulness under variation** — does it actually work for B and C, or only A?
- **Judgement about source data** — did you correctly figure out *where each value legitimately comes from*, including the values that aren't where you'd first look?
- **Document-engineering depth** — clean, structurally-valid Word output that survives Word, not a string-replace that happens to render.
- **Honesty** — your `SOLUTION.md` telling us exactly where it breaks is worth more than a confident tool that silently produces a wrong protocol. In this domain, a wrong-but-pretty document is the most dangerous possible output.

---

## 8. Deliverables checklist

- [ ] Source repo (generator + frontend), runnable per your README in ≤ 10 min.
- [ ] Generated outputs for **Set A, Set B, and Set C** (`.docx`), included in the repo.
- [ ] `SOLUTION.md` (architecture, run steps, assumptions, known failure modes).
- [ ] Anything you'd want a reviewer to know.

Submit a link (or archive) at the 48‑hour mark. Good luck.
