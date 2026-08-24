# Frontend Requirements

The frontend exists so we can run your generator **without reading your code**. Keep it minimal; we are not grading visual design. We are grading that the end-to-end path works on a clean machine.

## Must have

1. **One page.** Three file inputs, clearly labelled:
   - Test Method Procedure (`.docx`)
   - Acceptance Criteria & Limits (`.docx`)
   - Vendor Datasheet (`.pdf`)
2. An optional **Market** text field (defaults per `03_CQP_Field_and_Token_Reference.md` §D if left blank).
3. A **Generate** button that produces the protocol and lets us **download the `.docx`**.
4. Clear **error surfacing**: if generation fails, show the operator *why* (a stack trace dumped to the page is fine) — do not hand back a silently broken or empty document.
5. Works on **localhost** from your README. No deployment required.

## Nice to have (only if time allows — not required)

- A preview of the resolved values (cell model, manufacturer, the extracted electrical ratings, the detected duty profiles) **before** download, so the operator can sanity-check what was pulled from the inputs.
- A way to download the companion debug info (what your tool extracted from each source).

## Explicitly out of scope

- Authentication, accounts, persistence, multi-file batching, styling polish, mobile layout.
- Editing the protocol in the browser.

## How we will exercise it

We will open your page, upload **Set B**, then **Set C**, generate each, download the `.docx`, and open it in Microsoft Word. If a non-trivial fraction of fields are blank or wrong — most commonly the cell's electrical ratings — that set does not pass. A frontend that produces a polished page but a wrong document scores far below a plain page that produces a correct one.
