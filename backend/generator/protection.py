"""Document protection module - applies readOnly protection with permission markers."""
from __future__ import annotations
import zipfile
import os
import shutil
from lxml import etree
from docx.oxml.ns import qn


NSMAP = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def apply_document_protection(docx_path: str) -> None:
    """Apply readOnly protection with permission markers to match GOLD behavior."""
    tmp_path = docx_path + ".prot.tmp"

    with zipfile.ZipFile(docx_path, "r") as zin:
        with zipfile.ZipFile(tmp_path, "w") as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/settings.xml":
                    data = _add_protection_to_settings(data)
                elif item.filename == "word/document.xml":
                    data = _add_enforcement(data)
                zout.writestr(item, data)

    shutil.move(tmp_path, docx_path)


def _add_protection_to_settings(data: bytes) -> bytes:
    """Add documentProtection element to settings.xml."""
    root = etree.fromstring(data)
    wns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    existing = root.findall(f"{{{wns}}}documentProtection")
    for elem in existing:
        root.remove(elem)

    prot = etree.SubElement(root, f"{{{wns}}}documentProtection")
    prot.set(f"{{{wns}}}edit", "readOnly")
    prot.set(f"{{{wns}}}enforcement", "1")
    prot.set(f"{{{wns}}}formatting", "0")

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def _add_enforcement(data: bytes) -> bytes:
    """Ensure enforcement flag is set on permission markers."""
    root = etree.fromstring(data)
    wns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    for perm in root.findall(f"{{{wns}}}permStart"):
        perm.set(f"{{{wns}}}edit", "everyone")

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
