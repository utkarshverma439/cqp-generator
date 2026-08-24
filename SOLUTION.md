# SOLUTION.md — Cell Qualification Protocol Generator

> **Project Documentation**
>
> This document describes the design, implementation, and validation approach of the Cell Qualification Protocol (CQP) Generator.
>
> The solution automates CQP document generation from three source documents — TMP, ACL, and vendor Datasheet — using a structured parsing, normalization, validation, and DOCX generation pipeline.

**Author:** Utkarsh Verma  
**Project:** Cell Qualification Protocol (CQP) Generator
---

## Table of Contents

1. [How to Run It](#1-how-to-run-it)
2. [Architecture](#2-architecture)
3. [Implemented Features](#3-implemented-features)
4. [Assumptions Made](#4-assumptions-made)

---

## 1. How to Run It

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for building the frontend)

### Installation

```bash
# Clone the repository
git clone https://github.com/utkarshverma439/cqp-generator
cd cqp-generator

# Install Python backend dependencies
pip install -r requirements.txt

# Install frontend dependencies and build assets
cd frontend
npm install
npm run build
cd ..
```

### Running the Server

```bash
python run.py
```

The application will be available at **http://localhost:8000**.

### Using the Tool

1. Open http://localhost:8000 in a web browser
2. Upload three source documents:
   - **TMP** (.docx) — Test Method Procedure
   - **ACL** (.docx) — Acceptance Criteria & Limits
   - **Datasheet** (.pdf) — Vendor product datasheet
3. Select the target market (or leave blank for default)
4. Click **Generate CQP**
5. Download the generated .docx or preview it in-browser

### Development Mode

For hot-reloading during development:

```bash
# Terminal 1: Backend (port 8000)
python run.py

# Terminal 2: Frontend dev server (port 3000)
cd frontend
npm run dev
```

Access the development UI at http://localhost:3000 (requests are proxied to the backend).

---

## 2. Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React SPA)                     │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│    │ File     │ │ Market   │ │ Generate │ │ Preview  │          │
│    │ Upload   │ │ Select   │ │ Button   │ │ Modal    │          │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└───────────────────────────┬─────────────────────────────────────┘
                            │ POST /generate-cqp
                            │ (multipart/form-data)
┌───────────────────────────▼─────────────────────────────────────┐
│                    Backend (FastAPI)                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    main.py (API Layer)                   │   │
│  │  • File upload handling                                  │   │
│  │  • Temp file management                                  │   │
│  │  • Error response formatting                             │   │
│  │  • SPA static file serving                               │   │
│  └───────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────▼──────────────────────────────┐   │
│  │              cqp_service.py (Orchestrator)               │   │
│  │  • Coordinates the entire generation pipeline            │   │
│  └───┬──────────┬──────────┬──────────┬──────────┬──────────┘   │
│      │          │          │          │          │              │
│  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐          │
│  │  TMP  │  │  ACL  │  │ Data- │  │ Table │  │  Sec  │          │
│  │Parser │  │Parser │  │ sheet │  │   1   │  │   7   │          │
│  │       │  │       │  │Parser │  │  Gen  │  │  Gen  │          │
│  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘          │
│      │          │          │          │          │              │
│  ┌───▼──────────▼──────────▼──────────▼──────────▼──────────┐   │
│  │                    Normalizer                            │   │
│  │  • Merges 3 parser outputs into unified CellData model   │   │
│  └───────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────▼──────────────────────────────┐   │
│  │              Token Replacer + Footnote Handler           │   │
│  │  • Replaces {{ tokens }} in body, tables, headers/footers│   │
│  │  • Appends ACL footnotes before Revision Record          │   │
│  └───────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────▼──────────────────────────────┐   │
│  │              Protection (ZIP-level)                      │   │
│  │  • Applies readOnly protection to settings.xml           │   │
│  │  • Adds permission markers for editable reviewer zones   │   │
│  └───────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────▼──────────────────────────────┐   │
│  │              Validators (Input + Output)                 │   │
│  │  • Input: checks all CellData fields are populated       │   │
│  │  • Output: checks no tokens, correct row/block counts    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    Generated .docx file
```

### Backend Pipeline

The core generation flow follows a linear pipeline:

```
1. PARSE        Three independent parsers extract data from source documents
                 ├── TMP Parser: manufacturer, format, chemistry from pipe-delimited header
                 ├── ACL Parser: duty profiles, tests, limits, footnotes from XML body walking
                 └── Datasheet Parser: electrical ratings, grading from PDF text + OCR fallback

2. NORMALIZE    Merge three parser outputs into a single CellData model
                 ├── Extract cell model from document titles (after em-dash)
                 ├── Derive doc number from ACL doc ID (ACL- → CQP-)
                 └── Apply market selection from frontend

3. VALIDATE INPUT  Check all required fields are populated
                 ├── Cell model, manufacturer, chemistry, format, doc number
                 ├── Electrical ratings (nominal voltage, v_max, v_min, rated capacity)
                 ├── Grading (low, high)
                 └── Duty profiles (each has tests, rates, valid cycle count)

4. GENERATE DOCX   Build the output document
                 ├── Copy template to output path
                 ├── Replace simple {{ tokens }} in body, tables, headers/footers
                 ├── Remove template instruction paragraphs
                 ├── Generate Table 1 (Duty Profile Test Matrix) with vMerge
                 ├── Generate Section 7 blocks (per-profile test tables)
                 ├── Add footnotes before Revision Record
                 └── Apply document protection with editable reviewer zones

5. VALIDATE OUTPUT  Verify the generated document
                 ├── No unresolved {{ tokens }} remain
                 ├── Table 1 has correct number of data rows
                 ├── Section 7 has correct number of profile blocks
                 ├── Revision Record is blank (first row has "00", others empty)
                 └── Document protection exists with matching permStart/permEnd markers
```

### Frontend Architecture

Single-page React application with no routing:

```
App.tsx (State Management)
├── Header                    — Title banner with icon
├── UploadCard                — Card container for upload section
│   └── FileUpload (x3)       — Drag-and-drop zones for TMP, ACL, Datasheet
├── TargetMarketSelect        — Dropdown with Global/EU/US/Other options
├── GenerateButton            — CTA with loading spinner
├── GenerationSuccess         — Success card with download + preview buttons
├── DocumentPreview           — Modal with docx-preview rendering
├── ErrorMessage              — Error display with retry button
└── PrivacyNotice             — Footer privacy text
```

State is managed via `useState` hooks in `App.tsx` — no external state management library.

### Data Models (Pydantic)

```python
CellData                    # Unified model for all generation
├── cell_model: str
├── manufacturer: str
├── chemistry: str
├── cell_format: str
├── doc_number: str
├── framework: str          # "IESF-4400"
├── lab: str                # "Northgate Cell Qualification Laboratory (NCQL)"
├── market: str
├── electrical_ratings: ElectricalRatings
│   ├── nominal_voltage: str
│   ├── v_max: str
│   ├── v_min: str
│   └── rated_capacity: str
├── grading: Grading
│   ├── low: str
│   └── high: str
├── storage: str
├── supplied_as: str
├── duty_profiles: list[DutyProfile]
│   ├── name: str
│   ├── conditioning_rates: list[str]
│   ├── cycle_count: int
│   └── tests: list[TestEntry]
│       ├── sr_no: int
│       ├── test_name: str
│       ├── acceptance_limit: str
│       ├── clause: str
│       └── cycle_count: Optional[int]
└── footnotes: list[Footnote]
    ├── marker: str
    └── text: str
```

---

## 3. Implemented Features

### Core Functionality (All Complete)

| Feature | Status | Notes |
|---------|--------|-------|
| TMP Parser | ✅ Complete | Extracts manufacturer, format, chemistry from pipe-delimited header |
| ACL Parser | ✅ Complete | Walks XML body to associate profiles with test tables |
| Datasheet Parser | ✅ Complete | PyMuPDF text extraction + optional OCR fallback |
| Normalizer | ✅ Complete | Merges 3 outputs into unified CellData model |
| Token Replacement | ✅ Complete | Handles `{{ token }}` and `{{token}}` across body, tables, headers/footers |
| Table 1 Generation | ✅ Complete | Dynamic row expansion with vertical cell merging (vMerge) |
| Section 7 Generation | ✅ Complete | Per-profile test blocks built from raw OOXML elements |
| Footnote Handling | ✅ Complete | ACL footnotes placed before Revision Record |
| Document Protection | ✅ Complete | ZIP-level settings.xml modification with permission markers |
| Editable Reviewer Zones | ✅ Complete | Acceptance Criteria and Conclusion remain editable |
| Input Validation | ✅ Complete | Pre-generation field completeness checks |
| Output Validation | ✅ Complete | Post-generation structural verification |
| Template Instruction Removal | ✅ Complete | Helper text paragraphs removed from output |
| React Frontend | ✅ Complete | File upload, market selection, generate, download, preview |
| In-Browser DOCX Preview | ✅ Complete | docx-preview library renders generated document |
| Error Handling | ✅ Complete | Structured JSON error responses with details |

### Dynamic Behavior (Verified for All Sets)

| Requirement | How It's Handled |
|-------------|------------------|
| Different numbers of duty profiles | Parsers extract variable-length `duty_profiles` list; Table 1 and Section 7 expand dynamically |
| Different conditioning rates per profile | Each `DutyProfile` has its own `conditioning_rates` list; Table 1 creates one row per (profile × rate) |
| Different test lists per profile | Each profile has its own `tests` list; Section 7 block uses only that profile's tests |
| Different source-document wording | Parsers use regex patterns and fallback strategies, not hardcoded strings |
| Cell-specific numbers from datasheet | Electrical ratings and grading extracted via multi-strategy regex from PDF text |

### Set-Specific Results

| Set | Cell Model | Profiles | Rates | Tests | Status |
|-----|-----------|----------|-------|-------|--------|
| A | CYG-21700-50G | 2 | 4 | 10 | ✅ Generated |
| B | AUR-PR-340 | 1 | 2 | 8 | ✅ Generated |
| C | PLX-PCH-088 | 3 | 6 | 12 | ✅ Generated |

---

## 4. Assumptions Made

### Document Structure Assumptions

1. **TMP documents** have a pipe-delimited (`|`) header line in the second paragraph containing `manufacturer | format | chemistry`
2. **ACL documents** have "Duty Profile:" headings followed by their test tables in document order
3. **Datasheet PDFs** have extractable text on page 1 (manufacturer, format, chemistry) and page 3 (grading)
4. **Template structure** is fixed and not to be restructured (per assignment constraint)

### Data Extraction Assumptions

5. **Cell model** can be extracted from document titles after an em-dash (`—`) or double hyphen (`--`)
6. **Document number** is derived from ACL doc ID by replacing `ACL-` prefix with `CQP-`
7. **Chemistry format** should be normalized to `NMC811 / Graphite-SiOx` (cathode / anode with `/` separator)
8. **Cycle count** appears in the "Cycle-Life Endurance" test's acceptance limit as "after N cycles"

### Market Defaults

9. **Set A** defaults to `EU / UN-38.3`
10. **Set B** defaults to `US / DOT`
11. **Set C** defaults to `Global`
12. These are hardcoded in `config.py` and can be overridden via the frontend dropdown

### Technical Assumptions

13. **DOCX files** are valid ZIP archives with standard OOXML structure
14. **PDF text extraction** is sufficient for most datasheets (OCR is fallback, not primary)
15. **python-docx** handles basic DOCX operations; **lxml** is needed for advanced features (vMerge, protection)
16. **No external services** are required — all processing is local


---

## Appendix: Token-to-Source Mapping

| Token | Source | Parser |
|-------|--------|--------|
| `{{ doc_number }}` | Derived from ACL doc ID | normalizer.py |
| `{{ framework }}` | Constant: `IESF-4400` | config.py |
| `{{ lab }}` | Constant: `Northgate Cell Qualification Laboratory (NCQL)` | config.py |
| `{{ market }}` | Frontend input | App.tsx |
| `{{ cell_model }}` | Extracted from document titles | normalizer.py |
| `{{ manufacturer_from_datasheet }}` | Datasheet page 1 | datasheet_parser.py |
| `{{ format_from_datasheet }}` | Datasheet page 1 | datasheet_parser.py |
| `{{ chemistry }}` | Datasheet (normalized) | datasheet_parser.py |
| `{{ duty_profiles }}` | ACL profile names joined by ` & ` | acl_parser.py |
| `{{ tmp_doc_title }}` | TMP first paragraph | tmp_parser.py |
| `{{ acl_doc_title }}` | ACL first paragraph | acl_parser.py |
| `{{ datasheet_title }}` | Constructed: `{manufacturer} datasheet — {model}` | normalizer.py |
| `{{ nominal_voltage }}` | Datasheet electrical ratings | datasheet_parser.py |
| `{{ v_max }}` | Datasheet electrical ratings | datasheet_parser.py |
| `{{ v_min }}` | Datasheet electrical ratings | datasheet_parser.py |
| `{{ rated_capacity }}` | Datasheet electrical ratings | datasheet_parser.py |
| `{{ grading_low }}` | Datasheet page 3 | datasheet_parser.py |
| `{{ grading_high }}` | Datasheet page 3 | datasheet_parser.py |
| `{{ storage_from_datasheet }}` | Datasheet text | datasheet_parser.py |
| `{{ supplied_as_from_datasheet }}` | Datasheet text | datasheet_parser.py |

---

*This document fulfills the SOLUTION.md deliverable requirement from the assignment brief.*
