"""Token replacement engine for CQP generation."""
from __future__ import annotations
from docx import Document

from backend.generator.docx_utils import (
    replace_tokens_in_paragraph,
    replace_tokens_in_table,
    replace_tokens_in_header_footer,
)
from backend.models.cell_data import CellData


def build_token_map(data: CellData) -> dict[str, str]:
    """Build the complete token map from CellData."""
    duty_profiles_str = " & ".join(p.name for p in data.duty_profiles)

    return {
        "doc_number": data.doc_number,
        "framework": data.framework,
        "lab": data.lab,
        "market": data.market,
        "cell_model": data.cell_model,
        "manufacturer_from_datasheet": data.manufacturer,
        "format_from_datasheet": data.cell_format,
        "chemistry": data.chemistry,
        "duty_profiles": duty_profiles_str,
        "tmp_doc_title": data.tmp_title,
        "acl_doc_title": data.acl_title,
        "datasheet_title": data.datasheet_title,
        "nominal_voltage": data.electrical_ratings.nominal_voltage,
        "v_max": data.electrical_ratings.v_max,
        "v_min": data.electrical_ratings.v_min,
        "rated_capacity": data.electrical_ratings.rated_capacity,
        "grading_low": data.grading.low + " Ah",
        "grading_high": data.grading.high + " Ah",
        "storage_from_datasheet": data.storage,
        "supplied_as_from_datasheet": data.supplied_as,
    }


def replace_simple_tokens(doc: Document, token_map: dict[str, str]) -> None:
    """Replace all simple tokens in the document body, headers, and footers."""
    for paragraph in doc.paragraphs:
        replace_tokens_in_paragraph(paragraph, token_map)

    for table in doc.tables:
        replace_tokens_in_table(table, token_map)

    replace_tokens_in_header_footer(doc, token_map)
