"""TMP (Test Method Procedure) parser.

Extracts metadata from TMP documents. The parser is robust to varying
section heading names across different cell types.
"""
from __future__ import annotations
import re
from pathlib import Path
from docx import Document

from backend.models.cell_data import TMPData


def parse_tmp(file_path: str | Path) -> TMPData:
    """Parse a TMP .docx file and extract metadata."""
    doc = Document(str(file_path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    if len(paragraphs) < 2:
        raise ValueError(f"TMP document too short: {file_path}")

    title = paragraphs[0]

    # The second meaningful paragraph contains manufacturer | format | chemistry
    # This line uses '|' or '|' as separator
    header_line = _find_header_line(paragraphs)
    manufacturer, cell_format, chemistry = _parse_header_line(header_line)

    return TMPData(
        title=title,
        manufacturer=manufacturer,
        cell_format=cell_format,
        chemistry=chemistry,
    )


def _find_header_line(paragraphs: list[str]) -> str:
    """Find the metadata header line containing '|' separators.

    This line typically appears as the second paragraph and contains
    manufacturer | format | chemistry separated by '|' characters.
    """
    for i, text in enumerate(paragraphs[:5]):
        if '|' in text or '\u2502' in text:
            return text
        # Some TMPs use line breaks; check if next line has pipes
        if i + 1 < len(paragraphs) and ('|' in paragraphs[i + 1] or '\u2502' in paragraphs[i + 1]):
            return paragraphs[i + 1]

    # Fallback: look for lines with known manufacturer/format patterns
    for text in paragraphs[:5]:
        if any(kw in text.lower() for kw in ['cylindrical', 'prismatic', 'pouch', 'graphite', 'lfp', 'nmc']):
            return text

    raise ValueError("Could not find TMP header line with manufacturer/format/chemistry")


def _parse_header_line(line: str) -> tuple[str, str, str]:
    """Parse the header line to extract manufacturer, format, chemistry.

    Expected format: '<manufacturer> | <format> | <chemistry>'
    Variations: may use '|' or '|' or '/' as separators.
    """
    # Split on newline first to get just the first line of the header
    first_line = line.split('\n')[0].strip()

    # Normalize separators
    normalized = first_line.replace('\u2502', '|').replace('\r', '')

    # Split on '|'
    parts = [p.strip() for p in normalized.split('|') if p.strip()]

    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]

    if len(parts) == 2:
        # Might be "format | chemistry" without manufacturer
        # Try to extract manufacturer from context
        return parts[0], parts[1], ""

    # Single line - try comma or slash separation
    for sep in [',', '/', ';']:
        parts = [p.strip() for p in normalized.split(sep) if p.strip()]
        if len(parts) >= 3:
            return parts[0], parts[1], parts[2]

    raise ValueError(f"Cannot parse TMP header line: {line!r}")
