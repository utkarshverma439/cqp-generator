"""Pre-generation input validation."""
from __future__ import annotations
from pathlib import Path

from backend.models.cell_data import CellData


def validate_input(data: CellData) -> list[str]:
    """Validate CellData before generation. Returns list of errors."""
    errors = []

    if not data.cell_model:
        errors.append("cell_model is empty")
    if not data.manufacturer:
        errors.append("manufacturer is empty")
    if not data.chemistry:
        errors.append("chemistry is empty")
    if not data.cell_format:
        errors.append("cell_format is empty")
    if not data.doc_number:
        errors.append("doc_number is empty")

    er = data.electrical_ratings
    if not er.nominal_voltage:
        errors.append("nominal_voltage is empty")
    if not er.v_max:
        errors.append("v_max is empty")
    if not er.v_min:
        errors.append("v_min is empty")
    if not er.rated_capacity:
        errors.append("rated_capacity is empty")

    if not data.grading.low:
        errors.append("grading_low is empty")
    if not data.grading.high:
        errors.append("grading_high is empty")

    if not data.duty_profiles:
        errors.append("No duty profiles found")
    else:
        for i, profile in enumerate(data.duty_profiles):
            if not profile.conditioning_rates:
                errors.append(f"Profile '{profile.name}' has no conditioning rates")
            if not profile.tests:
                errors.append(f"Profile '{profile.name}' has no tests")
            if profile.cycle_count <= 0:
                errors.append(f"Profile '{profile.name}' has invalid cycle count: {profile.cycle_count}")

    return errors


def validate_files_exist(tmp_path: str, acl_path: str, ds_path: str) -> list[str]:
    """Check that all required input files exist."""
    errors = []
    for path, label in [(tmp_path, "TMP"), (acl_path, "ACL"), (ds_path, "Datasheet")]:
        if not Path(path).exists():
            errors.append(f"{label} file not found: {path}")
    return errors
