# CQP Template — Field & Token Reference

`CQP_Template.docx` contains `{{ token }}` placeholders and a few **repeated blocks**. This page tells you, for each one, **what value it must hold** and **which source document that value legitimately comes from**. It does *not* tell you how to extract it — that is the engineering.

> Ground truth for everything below is `reference_example/CQP_SetA_GOLD.docx`. If anything here is ambiguous, the gold wins.

---

## A. Simple tokens (one value per document)

| Token | Filled with | Source |
|---|---|---|
| `{{ doc_number }}` | Protocol document number (e.g. `CQP-CYG21700-00`) | Derived from the cell model; also appears in the ACL header |
| `{{ framework }}` | `IESF-4400` | Constant |
| `{{ lab }}` | `Northgate Cell Qualification Laboratory (NCQL)` | Constant |
| `{{ market }}` | Target market (e.g. `EU / UN-38.3`) | Provided per cell (see §D) |
| `{{ cell_model }}` | Cell model code | All three inputs / filename |
| `{{ manufacturer_from_datasheet }}` | Manufacturer name | **Datasheet** |
| `{{ format_from_datasheet }}` | Cell format (cylindrical / prismatic / pouch) | **Datasheet** |
| `{{ chemistry }}` | Cell chemistry | TMP / ACL header |
| `{{ duty_profiles }}` | All duty-profile names joined by ` & ` | **ACL** (its section structure) |
| `{{ tmp_doc_title }}` | Title of the TMP document | TMP |
| `{{ acl_doc_title }}` | Title of the ACL document | ACL |
| `{{ datasheet_title }}` | A reference label for the datasheet | Datasheet |

## B. Numeric tokens — the cell's electrical ratings

These define the qualification window and grading band. **They come from the vendor datasheet and from nowhere else** — the TMP and ACL deliberately defer to it. Open `DATASHEET_*.pdf` and locate each value.

| Token | Filled with | Where on the datasheet |
|---|---|---|
| `{{ nominal_voltage }}` | Nominal voltage (e.g. `3.63 V`) | Electrical ratings |
| `{{ v_max }}` | Maximum charge voltage (e.g. `4.20 V`) | Electrical ratings / discharge curve |
| `{{ v_min }}` | Minimum discharge cut-off (e.g. `2.50 V`) | Electrical ratings / discharge curve |
| `{{ rated_capacity }}` | Rated capacity (e.g. `5.00 Ah`) | Electrical ratings |
| `{{ grading_low }}` | Lowest graded capacity for the lot | Capacity-grading summary |
| `{{ grading_high }}` | Highest graded capacity for the lot | Capacity-grading summary |
| `{{ storage_from_datasheet }}` | Storage condition sentence | Datasheet |
| `{{ supplied_as_from_datasheet }}` | Packaging / supplied-as sentence | Datasheet |

> ⚠️ A blank or wrong value in this section fails the whole set (see Brief §5.2). These few numbers carry more grading weight than any other single thing in the document. Verify them against the gold for Set A before you trust your extraction on B and C.

## C. Repeated blocks (these grow with the cell)

### `{{ duty_profile }}`, `{{ rate }}`, `{{ cycles }}` — Table 1 (Duty Profile Test Matrix)
Table 1 has **one placeholder row** in the template. In the output it must become **one row per (duty profile × conditioning rate)**:
- `Sr. No.` numbered `1..N` across the whole table.
- The **Duty Profile** cell is **merged vertically** across that profile's rate rows (a profile with two rates occupies two rows but names the profile once). See the Set A gold.
- `Charge to` = `{{ v_max }}`, `Discharge to` = `{{ v_min }}`, `Cycles` = the cycle-life checkpoint count.

### Section 7 block — per duty profile
The `7.{{ block_index }} Qualification Tests — {{ duty_profile }}` heading and its table form **one block per duty profile**. For each profile:
- Replace the single `From the ACL …` placeholder row with **one row per test parameter** for *that* profile, taken from the ACL, numbered `1..n`.
- Carry the **Acceptance Limit** text verbatim, including any marker characters.
- Keep the per-block **`Acceptance Criteria:`** and **`Conclusion:`** paragraphs — these stay in the issued document for a reviewer to complete (see §E).

### `{{ also_fetch_any_footnotes_from_the_acl }}`
Replace with the ACL's footnote/note lines (the ones whose marker characters appear in the limit cells), verbatim, in order.

## D. Values supplied per run (frontend inputs)

A few values are not derivable from the documents and are entered by the operator in your frontend. For the three sample sets, use:

| Field | Set A | Set B | Set C |
|---|---|---|---|
| `market` | `EU / UN-38.3` | `US / DOT` | `Global` |

(If you prefer, your frontend may also let the operator confirm/override the cell model and document number, but the defaults above must be produced when the operator leaves them blank.)

## E. Tokens that must NOT be auto-filled

| Token / region | Required behaviour |
|---|---|
| `{{ to_be_added_by_reviewer }}` | Leave the *content* for a human, but the protocol's per-profile **Acceptance Criteria** and **Conclusion** blocks must remain **editable** after the document is locked for review. Everything else in the issued protocol is locked. |
| **Revision Record** table (end of document) | Stays **blank** at issue (revision `00`, no date/description/author). It is *not* a test table — do not place any test or specification data in it. |

---

## F. Acceptance summary (what "done" means for one cell)

1. No `{{ token }}` survives anywhere in the output.
2. Section B numeric values exactly match that cell's datasheet.
3. Table 1 and Section 7 expand to the cell's actual profile/rate/test structure, numbered correctly, with the profile cell merged in Table 1.
4. Limits, markers, clauses, and footnotes are carried verbatim from the ACL.
5. Formatting matches the template/gold; the file opens cleanly in Microsoft Word.
6. Reviewer zones editable; Revision Record blank.
