"""Datasheet PDF parser.

Extracts cell metadata from vendor datasheet PDFs using PyMuPDF.
Falls back to OCR for image-based tables.
"""
from __future__ import annotations
import re
import io
from pathlib import Path

import pymupdf
from PIL import Image

from backend.models.cell_data import DatasheetData, ElectricalRatings, Grading


def parse_datasheet(file_path: str | Path) -> DatasheetData:
    doc = pymupdf.open(str(file_path))
    if doc.page_count < 2:
        raise ValueError(f"Datasheet PDF too short: {file_path}")

    full_text = "\n".join(page.get_text() for page in doc)
    page1_text = doc[0].get_text() if doc.page_count > 0 else ""
    page3_text = doc[2].get_text() if doc.page_count > 2 else ""

    all_ocr_text = ""
    for page_idx in range(doc.page_count):
        images = _extract_page_images(doc, page_idx)
        for img in images:
            all_ocr_text += _ocr_image(img) + "\n"

    combined_text = full_text + "\n" + all_ocr_text

    manufacturer = _extract_manufacturer(page1_text, combined_text)
    cell_format, chemistry = _extract_format_and_chemistry(page1_text, combined_text)
    chemistry = _normalize_chemistry(chemistry)
    electrical_ratings = _extract_electrical_ratings(combined_text)
    grading = _extract_grading(page3_text, combined_text)
    storage = _extract_storage(combined_text)
    supplied_as = _extract_supplied_as(combined_text)
    title = f"{manufacturer} datasheet"

    doc.close()

    return DatasheetData(
        title=title,
        manufacturer=manufacturer,
        cell_format=cell_format,
        chemistry=chemistry,
        electrical_ratings=electrical_ratings,
        grading=grading,
        storage=storage,
        supplied_as=supplied_as,
    )


def _extract_page_images(doc, page_idx: int) -> list:
    """Extract images from a page as PIL Images."""
    images = []
    if page_idx >= doc.page_count:
        return images
    page = doc[page_idx]
    for img_info in page.get_images():
        xref = img_info[0]
        try:
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img = Image.open(io.BytesIO(img_bytes))
            images.append(img)
        except Exception:
            continue
    return images


def _ocr_image(img) -> str:
    """OCR an image using easyocr."""
    try:
        import numpy as np
        import easyocr
        img_np = np.array(img)
        reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        results = reader.readtext(img_np, detail=0)
        return "\n".join(results)
    except Exception:
        return ""


def _extract_manufacturer(page1: str, full_text: str) -> str:
    match = re.search(r"Manufactured by:\s*(.+?)[.\n]", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    for line in page1.split("\n"):
        line = line.strip()
        if line and len(line) > 3 and not line.startswith(("Product", "Model", "Electrical")):
            return line
    raise ValueError("Could not extract manufacturer from datasheet")


def _extract_format_and_chemistry(page1: str, full_text: str) -> tuple[str, str]:
    # Try direct regex on full text
    for sep in [",", ";"]:
        pattern = rf"Model\s+\S+\s*\(([^,{sep}]+)\s*[{sep}]\s*(.+?)\)"
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(2).strip().rstrip(")")

    # Try with extended context (join lines around Model keyword)
    lines = full_text.split("\n")
    for i, line in enumerate(lines):
        if "odel" in line.lower():
            context_lines = []
            for j in range(max(0, i - 4), min(len(lines), i + 5)):
                context_lines.append(lines[j].strip())
            combined = " ".join(context_lines)
            for sep in [",", ";"]:
                pattern = rf"Model\s+\S+\s*\(([^,{sep}]+)\s*[{sep}]\s*(.+?)\)"
                match = re.search(pattern, combined, re.IGNORECASE)
                if match:
                    return match.group(1).strip(), match.group(2).strip().rstrip(")")

    # Fallback: look for format keyword and chemistry in nearby text
    for fmt in ["cylindrical", "prismatic", "pouch"]:
        for sep in [",", ";"]:
            pattern = rf"\b{fmt}\s*[{sep}]"
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                start = max(0, match.start() - 100)
                end = min(len(full_text), match.end() + 100)
                context = full_text[start:end]
                chem_match = re.search(
                    r"((?:NMC|LFP)[\w/\s\-]*(?:Graphite|SiOx)?)",
                    context, re.IGNORECASE
                )
                if chem_match:
                    return fmt, chem_match.group(1).strip().rstrip(")")

    raise ValueError("Could not extract cell format and chemistry from datasheet")


def _normalize_chemistry(chem: str) -> str:
    """Ensure chemistry has proper format like 'NMC811 / Graphite-SiOx'."""
    # If already has / separator, return as-is
    if "/" in chem:
        return chem
    # Try to split NMC/LFP part from Graphite/SiOx part
    match = re.match(r"((?:NMC|LFP)\d*)(\s*)(Graphite.*)", chem, re.IGNORECASE)
    if match:
        nmc_part = match.group(1)
        graphite_part = match.group(3)
        return f"{nmc_part} / {graphite_part}"
    return chem


def _extract_electrical_ratings(full_text: str) -> ElectricalRatings:
    nv = _find_voltage(full_text, ["Nominal voltage", "nominal voltage"])
    vm = _find_voltage(full_text, ["Charge voltage", "charge voltage"])
    vmin = _find_voltage(full_text, ["Discharge cut-off", "discharge cut-off"])
    rc = _find_capacity(full_text)
    if not nv:
        raise ValueError("Could not extract nominal voltage")
    if not vm:
        raise ValueError("Could not extract max charge voltage")
    if not vmin:
        raise ValueError("Could not extract min discharge voltage")
    if not rc:
        raise ValueError("Could not extract rated capacity")
    return ElectricalRatings(nominal_voltage=nv, v_max=vm, v_min=vmin, rated_capacity=rc)


def _find_voltage(text: str, keywords: list[str]) -> str:
    lines = text.split("\n")
    for kw in keywords:
        for i, line in enumerate(lines):
            if kw.lower() in line.lower():
                # Check same line
                m = re.search(r"(\d+\.?\d*)\s*V", line)
                if m:
                    return f"{m.group(1)} V"
                # Check next line first (text extraction: value after label)
                if i + 1 < len(lines):
                    m = re.search(r"(\d+\.?\d*)\s*V", lines[i + 1])
                    if m:
                        return f"{m.group(1)} V"
                # Check previous line (OCR table: value before label)
                if i - 1 >= 0:
                    m = re.search(r"(\d+\.?\d*)\s*V", lines[i - 1])
                    if m:
                        return f"{m.group(1)} V"
    # Fallback: look for voltage value near "cut" keyword on adjacent lines
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if "cut" in line_lower:
            for j in range(i, min(i + 3, len(lines))):
                match = re.search(r"(\d+\.?\d*)\s*V", lines[j])
                if match:
                    return f"{match.group(1)} V"
    return ""


def _find_capacity(text: str) -> str:
    match = re.search(r"Rated\s+capacity.*?(\d+\.?\d*)\s*Ah", text, re.IGNORECASE | re.DOTALL)
    if match:
        return f"{match.group(1)} Ah"
    # OCR may put capacity value on line before "Rated capacity"
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "rated capacity" in line.lower():
            for j in range(max(0, i - 3), i + 1):
                m = re.search(r"(\d+\.?\d*)\s*Ah", lines[j])
                if m:
                    return f"{m.group(1)} Ah"
    match = re.search(r"(\d+\.?\d*)\s*Ah.*?0\.5C", text)
    if match:
        return f"{match.group(1)} Ah"
    return ""


def _extract_grading(page3: str, full_text: str) -> Grading:
    search_text = page3 if page3.strip() else full_text

    low = _find_grading_value(search_text, "Lowest graded capacity")
    high = _find_grading_value(search_text, "Highest graded capacity")

    if not low or not high:
        low = _find_grading_value(full_text, "Lowest graded capacity")
        high = _find_grading_value(full_text, "Highest graded capacity")

    if not low or not high:
        raise ValueError("Could not extract grading information")
    return Grading(low=low, high=high)


def _find_grading_value(text: str, keyword: str) -> str:
    """Find a grading value near the keyword.

    Handles cases where the value is on the same line or a nearby line.
    """
    # Try same-line extraction first
    pattern = rf"{re.escape(keyword)}.*?(\d+\.?\d*)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1)

    # Try line-by-line extraction
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            # Check same line first
            match = re.search(r"(\d+\.?\d*)", line)
            if match and keyword.lower() not in line.lower().replace(match.group(1), ""):
                pass  # Skip if the number is part of the keyword itself
            # Check next few lines
            for j in range(1, 4):
                if i + j < len(lines):
                    match = re.search(r"(\d+\.?\d*)", lines[i + j])
                    if match:
                        return match.group(1)
    return ""


def _extract_storage(full_text: str) -> str:
    match = re.search(r"(Store\s+at.+?)(?:\n|$)", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"(Keep\s+at.+?)(?:\n|$)", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"(\d+\s*\xb1?\s*\d+\s*\xb0?\s*C.+?(?:SOC|charge).+?)(?:\n|$)", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def _extract_supplied_as(full_text: str) -> str:
    match = re.search(r"(Supplied\s+as.+?)(?:\n|$)", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"(Provided\s+as.+?)(?:\n|$)", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"(Delivered\s+as.+?)(?:\n|$)", full_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""
