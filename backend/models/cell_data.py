"""Pydantic data models for CQP Generator."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class ElectricalRatings(BaseModel):
    nominal_voltage: str
    v_max: str
    v_min: str
    rated_capacity: str


class Grading(BaseModel):
    low: str
    high: str


class TestEntry(BaseModel):
    sr_no: int
    test_name: str
    acceptance_limit: str  # VERBATIM from ACL, including markers
    clause: str
    cycle_count: Optional[int] = None


class DutyProfile(BaseModel):
    name: str
    conditioning_rates: list[str]
    cycle_count: int
    tests: list[TestEntry]


class Footnote(BaseModel):
    marker: str
    text: str


class TMPData(BaseModel):
    title: str
    manufacturer: str
    chemistry: str
    cell_format: str


class ACLData(BaseModel):
    title: str
    doc_id: str
    manufacturer: str
    duty_profiles: list[DutyProfile]
    footnotes: list[Footnote]


class DatasheetData(BaseModel):
    title: str
    manufacturer: str
    cell_format: str
    chemistry: str
    electrical_ratings: ElectricalRatings
    grading: Grading
    storage: str
    supplied_as: str


class CellData(BaseModel):
    cell_model: str
    manufacturer: str
    chemistry: str
    cell_format: str
    doc_number: str
    framework: str
    lab: str
    market: str
    tmp_title: str
    acl_title: str
    datasheet_title: str
    electrical_ratings: ElectricalRatings
    grading: Grading
    storage: str
    supplied_as: str
    duty_profiles: list[DutyProfile]
    footnotes: list[Footnote]
