"""Section 7 generator - creates per-duty-profile test blocks."""
from __future__ import annotations
from docx import Document
from docx.table import Table
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree

from backend.models.cell_data import CellData, DutyProfile
from backend.config import FRAMEWORK, ACCEPTANCE_CRITERIA_TEXT, CONCLUSION_TEXT


def generate_section7(doc: Document, data: CellData) -> None:
    """Generate all Section 7 blocks for each duty profile."""
    _remove_template_block(doc)
    _remove_template_footnotes(doc)
    insert_point = _find_section7_insert_point(doc)
    perm_id = 1
    for idx, profile in enumerate(data.duty_profiles):
        block = _create_profile_block(profile, idx + 1, perm_id)
        perm_id += 2
        for elem in block:
            insert_point.addprevious(elem)


def _remove_template_block(doc: Document) -> None:
    body = doc.element.body
    elements = list(body)
    in_block = False
    to_remove = []
    for elem in elements:
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "p":
            txt = "".join(t.text for t in elem.iter() if t.tag.endswith("}t") and t.text)
            if "7.{{ block_index }}" in txt or "7.{{block_index}}" in txt:
                in_block = True
                to_remove.append(elem)
                continue
        if in_block:
            if tag == "tbl":
                to_remove.append(elem)
            elif tag == "p":
                txt = "".join(t.text for t in elem.iter() if t.tag.endswith("}t") and t.text)
                to_remove.append(elem)
                if "also_fetch_any_footnotes" in txt:
                    break
            else:
                break
    for elem in to_remove:
        body.remove(elem)


def _remove_template_footnotes(doc: Document) -> None:
    body = doc.element.body
    for p in list(body.iter(qn("w:p"))):
        txt = "".join(t.text for t in p.iter() if t.tag.endswith("}t") and t.text)
        if "also_fetch_any_footnotes" in txt:
            parent = p.getparent()
            if parent is not None:
                parent.remove(p)


def _find_section7_insert_point(doc: Document):
    body = doc.element.body
    elements = list(body)
    found_heading = False
    for elem in elements:
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "p":
            txt = "".join(t.text for t in elem.iter() if t.tag.endswith("}t") and t.text)
            if "7. Qualification Test Parameters" in txt:
                found_heading = True
                continue
            if found_heading:
                return elem
    raise ValueError("Could not find Section 7 insertion point")


def _create_profile_block(profile: DutyProfile, block_index: int, perm_id: int) -> list:
    elements = []
    elements.append(_make_heading(profile.name, block_index))
    elements.append(_make_test_table(profile))
    elements.append(_make_bold_p("Acceptance Criteria:"))
    elements.append(_make_perm_start(perm_id))
    elements.append(_make_normal_p(ACCEPTANCE_CRITERIA_TEXT))
    elements.append(_make_perm_end(perm_id))
    elements.append(_make_bold_p("Conclusion:"))
    elements.append(_make_perm_start(perm_id + 1))
    elements.append(_make_normal_p(CONCLUSION_TEXT))
    elements.append(_make_perm_end(perm_id + 1))
    elements.append(OxmlElement("w:p"))
    return elements


def _make_heading(name: str, idx: int) -> etree._Element:
    p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    p.append(pPr)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    b = OxmlElement("w:b")
    rPr.append(b)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "24")
    rPr.append(sz)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "1F3A5F")
    rPr.append(color)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = f"7.{idx} Qualification Tests \u2014 {name}"
    r.append(t)
    p.append(r)
    return p


def _make_test_table(profile: DutyProfile) -> etree._Element:
    tbl = OxmlElement("w:tbl")
    tblPr = OxmlElement("w:tblPr")
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), "9936")
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)
    tblBorders = OxmlElement("w:tblBorders")
    for bn in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        border = OxmlElement(f"w:{bn}")
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "4")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), "000000")
        tblBorders.append(border)
    tblPr.append(tblBorders)
    tbl.append(tblPr)

    tblGrid = OxmlElement("w:tblGrid")
    for _ in range(4):
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), "2484")
        tblGrid.append(gc)
    tbl.append(tblGrid)

    headers = ["Sr. No.", "Test Parameter", "Acceptance Limit", f"{FRAMEWORK} Clause"]
    tbl.append(_make_header_row(headers))

    for i, test in enumerate(profile.tests, start=1):
        tbl.append(_make_data_row([
            str(i), test.test_name, test.acceptance_limit, test.clause
        ]))

    return tbl


def _make_header_row(headers: list[str]) -> etree._Element:
    tr = OxmlElement("w:tr")
    for h in headers:
        tc = OxmlElement("w:tc")
        tcPr = OxmlElement("w:tcPr")
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "1F3A5F")
        tcPr.append(shd)
        tc.append(tcPr)
        p = OxmlElement("w:p")
        pPr = OxmlElement("w:pPr")
        jc = OxmlElement("w:jc")
        jc.set(qn("w:val"), "center")
        pPr.append(jc)
        p.append(pPr)
        r = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        b = OxmlElement("w:b")
        rPr.append(b)
        i_elem = OxmlElement("w:i")
        i_elem.set(qn("w:val"), "0")
        rPr.append(i_elem)
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "20")
        rPr.append(sz)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "FFFFFF")
        rPr.append(color)
        r.append(rPr)
        t = OxmlElement("w:t")
        t.text = h
        r.append(t)
        p.append(r)
        tc.append(p)
        tr.append(tc)
    return tr


def _make_data_row(values: list[str]) -> etree._Element:
    tr = OxmlElement("w:tr")
    for v in values:
        tc = OxmlElement("w:tc")
        p = OxmlElement("w:p")
        r = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        b = OxmlElement("w:b")
        b.set(qn("w:val"), "false")
        rPr.append(b)
        i_elem = OxmlElement("w:i")
        i_elem.set(qn("w:val"), "0")
        rPr.append(i_elem)
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "20")
        rPr.append(sz)
        r.append(rPr)
        t = OxmlElement("w:t")
        t.text = v
        r.append(t)
        p.append(r)
        tc.append(p)
        tr.append(tc)
    return tr


def _make_bold_p(text: str) -> etree._Element:
    p = OxmlElement("w:p")
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    b = OxmlElement("w:b")
    rPr.append(b)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    r.append(t)
    p.append(r)
    return p


def _make_normal_p(text: str) -> etree._Element:
    p = OxmlElement("w:p")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = text
    r.append(t)
    p.append(r)
    return p


def _make_perm_start(perm_id: int) -> etree._Element:
    elem = OxmlElement("w:permStart")
    elem.set(qn("w:id"), str(perm_id))
    elem.set(qn("w:edit"), "everyone")
    return elem


def _make_perm_end(perm_id: int) -> etree._Element:
    elem = OxmlElement("w:permEnd")
    elem.set(qn("w:id"), str(perm_id))
    return elem
