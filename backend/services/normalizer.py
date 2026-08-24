"""Normalizer: combines parser outputs into a single CellData model."""
from __future__ import annotations
import re
from backend.models.cell_data import (
    CellData, TMPData, ACLData, DatasheetData, ElectricalRatings, Grading,
)
from backend.config import FRAMEWORK, LAB


def normalize(tmp: TMPData, acl: ACLData, ds: DatasheetData, market: str) -> CellData:
    cell_model = _extract_model(tmp.title, acl.title)
    doc_number = _derive_doc_number(acl)
    datasheet_title = f"{ds.manufacturer} datasheet \u2014 {cell_model}"

    return CellData(
        cell_model=cell_model,
        manufacturer=ds.manufacturer,
        chemistry=ds.chemistry,
        cell_format=ds.cell_format,
        doc_number=doc_number,
        framework=FRAMEWORK,
        lab=LAB,
        market=market,
        tmp_title=tmp.title,
        acl_title=acl.title,
        datasheet_title=datasheet_title,
        electrical_ratings=ds.electrical_ratings,
        grading=ds.grading,
        storage=ds.storage,
        supplied_as=ds.supplied_as,
        duty_profiles=acl.duty_profiles,
        footnotes=acl.footnotes,
    )


def _extract_model(tmp_title: str, acl_title: str) -> str:
    for title in [tmp_title, acl_title]:
        match = re.search(r"\u2014\s*(.+?)$", title)
        if match:
            return match.group(1).strip()
        match = re.search(r"--\s*(.+?)$", title)
        if match:
            return match.group(1).strip()
        match = re.search(r"[\u2014\u2013-]\s*(.+?)$", title)
        if match:
            return match.group(1).strip()
    raise ValueError("Could not extract cell model from document titles")


def _derive_doc_number(acl: ACLData) -> str:
    if acl.doc_id:
        return acl.doc_id.replace("ACL-", "CQP-", 1)
    raise ValueError("Could not derive document number: no ACL doc_id found")
