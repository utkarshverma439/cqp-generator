"""Footnote handler - places ACL footnotes after the last Section 7 block."""
from __future__ import annotations
from lxml import etree
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from backend.models.cell_data import CellData


def add_footnotes(doc: Document, data: CellData) -> None:
    """Add ACL footnotes after the last Section 7 block, before Revision Record."""
    if not data.footnotes:
        return

    insert_before = _find_revision_record(doc)
    body = doc.element.body
    idx = list(body).index(insert_before)

    empty_p = OxmlElement("w:p")
    body.insert(idx, empty_p)
    idx += 1

    label_p = OxmlElement("w:p")
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    b = OxmlElement("w:b")
    rPr.append(b)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = "Applicable notes from the ACL:"
    r.append(t)
    label_p.append(r)
    body.insert(idx, label_p)
    idx += 1

    for fn in data.footnotes:
        p = OxmlElement("w:p")
        r = OxmlElement("w:r")
        t = OxmlElement("w:t")
        t.text = f"{fn.marker} {fn.text}"
        r.append(t)
        p.append(r)
        body.insert(idx, p)
        idx += 1


def _find_revision_record(doc: Document):
    body = doc.element.body
    for elem in body:
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "p":
            txt = "".join(t.text for t in elem.iter() if t.tag.endswith("}t") and t.text)
            if "Revision Record" in txt:
                return elem
    raise ValueError("Could not find Revision Record heading")
