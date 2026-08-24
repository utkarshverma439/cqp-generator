# Domain Primer — Cell Qualification, in plain language

You do **not** need a background in batteries or regulation. This page gives you everything the assignment assumes. Read it once; refer back as needed. (The framework, the lab, the manufacturers, and the cells below are all fictional — this is a self-contained world invented for this exercise.)

---

## The world

A laboratory called **NCQL** (Northgate Cell Qualification Laboratory) is paid to **qualify** rechargeable battery cells. "Qualifying" a cell means: run a defined battery of tests on it, check each result against a pass/fail limit, and issue a signed document certifying the cell for use. That document is the **Cell Qualification Protocol (CQP)** — the thing your program must produce.

All of this happens under a rulebook called **IESF‑4400** (think of it as the "standard" everyone cites; its clauses look like `§6.2`, `§6.3`, …). You never have to interpret the rulebook — you just have to carry its clause numbers through from the inputs to the output.

---

## The three source documents

For each cell, three documents arrive. Your generator reads all three and merges them into the protocol.

### 1. TMP — Test Method Procedure (`TMP_*.docx`)
The **method**: *how* each test is performed (equipment, conditioning steps, procedure, data handling). It is prose with section headings. Different cells' TMPs are written by different authors, so **the same section can have different headings** (e.g. one says "Cell Conditioning Sequence," another says "Pre‑Test Conditioning," another "Sample Preparation and Formation" — all the same thing). The TMP tells you the *shape* of the work but deliberately does **not** restate the cell's numeric ratings.

### 2. ACL — Acceptance Criteria & Limits (`ACL_*.docx`)
The **limits**: a set of tables, **one section per duty profile**, each listing the test parameters and their acceptance limits (e.g. "Capacity Verification — ≥ 98.0 % of rated capacity," "DCIR — ≤ 18 mΩ"). Some limit rows carry a **marker** character (`*`, `#`, `@`, `$`); the matching note is printed at the foot of the ACL. Markers and their notes must travel into the protocol unchanged.

### 3. Datasheet (`DATASHEET_*.pdf`)
The cell **vendor's product datasheet**. This is where the cell's actual **electrical ratings** live — nominal voltage, maximum charge voltage, minimum discharge cut-off, rated capacity — together with a **discharge curve** and a **production capacity‑grading summary** (the lowest and highest graded capacity for the lot). It also carries the manufacturer name, storage condition, and packaging. These ratings are specific to each cell and appear **nowhere else** in the inputs — the TMP and ACL both defer to "the vendor datasheet" for them. Getting these numbers onto the protocol correctly is central to the task; open the datasheet and see what you're dealing with.

---

## Two structural ideas you must handle

### Duty profiles
A **duty profile** is an intended use of the cell — "Automotive Traction," "Grid Storage," "Aerospace Auxiliary," etc. A cell is qualified for **one or more** duty profiles, and *each profile can have its own test list and its own limits.* The number of profiles varies from cell to cell — this is the main axis along which the protocol grows or shrinks.

### Conditioning rates
Within a duty profile, the cell is exercised at one or more **conditioning rates** (charge/discharge speeds, written like `0.5C`, `1.0C`). A profile with two rates produces two rows in the test matrix; a profile with one rate produces one. In the protocol's **Duty Profile Test Matrix (Table 1)**, the profile name spans (is merged across) all of its rate rows — look at the Set A gold to see exactly how.

---

## The qualification tests (you only carry these through; you don't run them)

You'll see names like Capacity Verification, DC Internal Resistance (DCIR), Cycle‑Life Endurance, Overcharge Tolerance, Forced Over‑Discharge, External Short‑Circuit, Thermal Stability (Hot‑Box), Altitude Simulation, Insulation Resistance. Each comes from the ACL with a limit and an `IESF‑4400` clause. Your job is **not** to evaluate them — only to place the right rows, for the right duty profile, into the right table, with their markers and clauses intact.

---

## How the protocol is organised (the template)

`CQP_Template.docx` is the fixed shell. Top to bottom: title block → Purpose → Scope → Reference Documents → **Test Article Description** (the datasheet ratings) → Conditioning & Test Window → **Duty Profile Test Matrix (Table 1)** → **Section 7: per‑duty‑profile test tables** (each with an *Acceptance Criteria* and *Conclusion* block a reviewer fills in later) → a **Revision Record** at the very end that is left blank at issue.

The template is marked up with `{{ tokens }}`. **`03_CQP_Field_and_Token_Reference.md` lists every token and the source it must be filled from.** Your generator's job, in one sentence: *resolve every token and expand every repeated block, for any cell, so the result matches what a careful human would have produced by hand* — which, for Set A, is exactly `CQP_SetA_GOLD.docx`.
