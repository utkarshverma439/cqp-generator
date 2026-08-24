# 📄 Cell Qualification Protocol Generator

> A dynamic end-to-end tool that extracts specifications from three source documents (TMP, ACL, and Vendor Datasheet) for battery cells and generates a professionally formatted **Cell Qualification Protocol** `.docx` conforming to the **IESF-4400** standard framework.

---

## 🚀 Key Features

*   **Document Parsing**: Parses `.docx` structures for Test Method Procedures (TMP) and Acceptance Criteria & Limits (ACL), and `.pdf` files (with automated OCR fallback) for Datasheet specifications.
*   **Automatic Normalization**: Maps disparate input schemas into a unified, type-safe data model.
*   **Dynamic Document Generation**: Clones template files and generates complex OOXML elements including vertically-merged tables (Duty Profile Test Matrix) and duplicated test detail blocks.
*   **Client-Side Preview**: Enables operators to preview the generated protocol directly in the browser using high-fidelity client-side rendering before downloading.
*   **Security & Protection**: Automatically locks the output protocol except for reviewer comment areas (Acceptance Criteria & Conclusion zones), preserving document integrity.

---

## 🛠️ Stack

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.2-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=flat-square&logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?style=flat-square&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)

---

## 📁 Repository Structure

```
cqp-generator/
├── backend/
│   ├── __init__.py                # Package marker
│   ├── main.py                    # FastAPI server (API endpoints & SPA serving)
│   ├── config.py                  # Global constants & template/output path settings
│   ├── .env.example               # Environment variable template for backend config
│   ├── models/
│   │   ├── __init__.py
│   │   └── cell_data.py           # Pydantic data models for cell specifications
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── tmp_parser.py          # Test Method Procedure (.docx) parser
│   │   ├── acl_parser.py          # Acceptance Criteria & Limits (.docx) parser
│   │   └── datasheet_parser.py    # Datasheet (.pdf) parser with easyocr fallback
│   ├── services/
│   │   ├── __init__.py
│   │   ├── normalizer.py          # Combines parsed inputs into a normalized schema
│   │   └── cqp_service.py         # Orchestrator coordinating parsing, generation, and validation
│   ├── generator/
│   │   ├── __init__.py
│   │   ├── token_replacer.py      # Inline template token replacement engine
│   │   ├── table1_generator.py    # Generates the Duty Profile Test Matrix with vertical cell merging
│   │   ├── section7_generator.py  # Generates duplicated section blocks per duty profile
│   │   ├── footnote_handler.py    # Appends active footnotes referencing ACL markers
│   │   ├── protection.py          # Applies read-only protection with reviewer exceptions
│   │   └── docx_utils.py          # Low-level OOXML helper utilities
│   └── validators/
│       ├── __init__.py
│       ├── input_validator.py     # Validation for parsed input fields
│       └── output_validator.py    # Structure verification on generated DOCX output
├── frontend/
│   ├── .env                       # Vite environment variables (API_BASE_URL)
│   ├── .env.example               # Environment variable template for frontend config
│   ├── index.html                 # Application entrypoint
│   ├── package.json               # Frontend dependency declarations
│   ├── package-lock.json          # Locked dependency versions
│   ├── vite.config.ts             # Vite build config & dev server proxy
│   ├── tsconfig.json              # TypeScript compiler configuration
│   ├── tailwind.config.js         # TailwindCSS content paths
│   ├── postcss.config.js          # PostCSS plugins (Tailwind, Autoprefixer)
│   ├── dist/                      # Built production assets (served by FastAPI)
│   └── src/
│       ├── main.tsx               # React root render
│       ├── App.tsx                # Main application layout & generation state logic
│       ├── index.css              # TailwindCSS directives & base styles
│       ├── vite-env.d.ts          # Vite environment type declarations
│       └── components/
│           ├── Header.tsx         # Title banner with icon
│           ├── UploadCard.tsx     # Card container for upload section
│           ├── FileUpload.tsx     # Drag-and-drop file upload with Word/PDF icons
│           ├── TargetMarketSelect.tsx  # Market dropdown with "Other" text field
│           ├── GenerateButton.tsx # Generate CTA with loading spinner
│           ├── GenerationSuccess.tsx   # Success card with download + preview buttons
│           ├── DocumentPreview.tsx # Modal with docx-preview rendering
│           ├── ErrorMessage.tsx   # Error display with retry button
│           └── PrivacyNotice.tsx  # Footer privacy text
├── docs/
│   ├── 00_START_HERE.md           # Assignment onboarding guide
│   ├── 01_Assignment_Brief.md     # Full assignment specification
│   ├── 02_Domain_Primer.md        # Battery cell qualification domain explanation
│   ├── 03_CQP_Field_and_Token_Reference.md  # Template token-to-source mapping
│   └── 04_Frontend_Requirements.md  # UI specification
├── inputs/
│   ├── setA/                      # CYG-21700-50G (2 profiles, 4 rates)
│   │   ├── TMP_CYG-21700-50G.docx
│   │   ├── ACL_CYG-21700-50G.docx
│   │   └── DATASHEET_CYG-21700-50G.pdf
│   ├── setB/                      # AUR-PR-340 (1 profile, 2 rates)
│   │   ├── TMP_AUR-PR-340.docx
│   │   ├── ACL_AUR-PR-340.docx
│   │   └── DATASHEET_AUR-PR-340.pdf
│   └── setC/                      # PLX-PCH-088 (3 profiles, 6 rates)
│       ├── TMP_PLX-PCH-088.docx
│       ├── ACL_PLX-PCH-088.docx
│       └── DATASHEET_PLX-PCH-088.pdf
├── outputs/                       # Generated CQP documents (gitignored)
├── reference_example/
│   └── CQP_SetA_GOLD.docx        # Reference target protocol output for Set A
├── template/
│   └── CQP_Template.docx          # Base Microsoft Word layout template
├── .gitignore                     # Git ignore rules
├── LICENSE                        # License file
├── README.md                      # This file
├── SOLUTION.md                    # Architecture and assumptions
├── requirements.txt               # Python backend dependencies
└── run.py                         # Entry point helper to run the server
```

---

## ⚙️ Quick Start

### 1. Prerequisites
Ensure you have the following installed on your machine:
*   **Python 3.11+**
*   **Node.js 18+**

### 2. Installation & Setup
Clone the repository and install dependencies for both components:

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

### 3. Run the Application
Start the unified server using the startup script:
```bash
python run.py
```
*   The application will be served at: **[http://localhost:8000](http://localhost:8000)**

---

## 🧑‍💻 Development Workflow

To run with hot-reloading enabled for both the backend and frontend:

### Start the Backend Server (Port 8000)
```bash
python run.py
```

### Start the Frontend Dev Server (Port 3000)
In a separate terminal shell:
```bash
cd frontend
npm run dev
```
*   Access the live development application at **[http://localhost:3000](http://localhost:3000)** (requests are proxied to the backend automatically).

---

## 📋 Supported Datasets

The application is pre-calibrated to process and validate three standard reference sets:

| Set | Cell Model | Application Profiles | Target Market (Default) |
|:---:|:---|:---|:---|
| **A** | `CYG-21700-50G` | Automotive Traction, Grid Storage | `EU / UN-38.3` |
| **B** | `AUR-PR-340` | Aerospace Auxiliary | `US / DOT` |
| **C** | `PLX-PCH-088` | Automotive Traction, Grid Storage, Consumer Electronics | `Global` |

---

## 📡 API Reference

### GET `/health`
Returns server status check.
*   **Response**: `{"status": "ok"}`

### POST `/generate-cqp`
Generates a Cell Qualification Protocol from uploaded source files.
*   **Request Type**: `multipart/form-data`
*   **Parameters**:

| Field | Type | Required | Description |
|:---|:---:|:---:|:---|
| `tmp_file` | File (`.docx`) | **Yes** | Test Method Procedure document |
| `acl_file` | File (`.docx`) | **Yes** | Acceptance Criteria & Limits document |
| `datasheet_file` | File (`.pdf`) | **Yes** | Cell Manufacturer Datasheet |
| `market` | String | *No* | Target market designation (defaults to `Global`) |

*   **Response**: Returns the generated `.docx` binary file directly as an attachment stream.

---

## 🛡️ License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Utkarsh Verma
