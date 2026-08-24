"""Configuration constants for CQP Generator."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CANDIDATE_PACK_DIR = BASE_DIR.parent / "candidate_pack"

# Paths — use environment variables if set, otherwise fall back to defaults
TEMPLATE_PATH = Path(os.getenv("TEMPLATE_PATH", str(CANDIDATE_PACK_DIR / "template" / "CQP_Template.docx")))
INPUTS_DIR = Path(os.getenv("INPUTS_DIR", str(CANDIDATE_PACK_DIR / "inputs")))
OUTPUTS_DIR = Path(os.getenv("OUTPUTS_DIR", str(BASE_DIR / "outputs")))

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Framework and lab constants
FRAMEWORK = os.getenv("FRAMEWORK", "IESF-4400")
LAB = os.getenv("LAB", "Northgate Cell Qualification Laboratory (NCQL)")

MARKET_DEFAULTS = {
    "CYG-21700-50G": "EU / UN-38.3",
    "AUR-PR-340": "US / DOT",
    "PLX-PCH-088": "Global",
}

ACCEPTANCE_CRITERIA_TEXT = "All listed parameters meet the acceptance limits for this duty profile."
CONCLUSION_TEXT = "The cell is qualified for this duty profile, subject to review."
