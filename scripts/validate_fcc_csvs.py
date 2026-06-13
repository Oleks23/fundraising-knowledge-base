#!/usr/bin/env python3
"""Validate FCC CSV files against templates and core model rules."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = REPO_ROOT / "data" / "sample"
TEMPLATE_DIR = REPO_ROOT / "data" / "templates"

ID_COLUMNS = {
    "programs.csv": "program_id",
    "initiatives.csv": "initiative_id",
    "commitments.csv": "commitment_id",
    "dependencies.csv": "dependency_id",
    "risks.csv": "risk_id",
    "knowledge.csv": "knowledge_id",
    "metric_snapshots.csv": "snapshot_id",
    "configuration.csv": "config_id",
}

DATE_COLUMNS = {
    "programs.csv": ["start_date", "end_date"],
    "initiatives.csv": ["start_date", "target_date"],
    "commitments.csv": ["due_date"],
    "dependencies.csv": ["due_date"],
    "risks.csv": ["date_identified", "target_resolution_date"],
    "knowledge.csv": ["review_date"],
    "metric_snapshots.csv": ["snapshot_date"],
    "configuration.csv": ["effective_date"],
}

# Canonical status values come from CANONICAL_DATA_MODEL.md and
# SHAREPOINT_LISTS_DESIGN.md. STATUS_ALIASES below are accepted only as import
# normalization aliases; they should be normalized before production load.
STATUS_VALUES = {
    "programs.csv": {"Active", "Inactive"},
    "initiatives.csv": {"Active", "Complete", "On Hold", "At Risk"},
    "commitments.csv": {"Open", "Completed", "Overdue"},
    "dependencies.csv": {"Open", "Resolved"},
    "risks.csv": {"Open", "Monitoring", "Resolved"},
    "knowledge.csv": {"Draft", "Approved", "Archived"},
    "configuration.csv": {"Active", "Inactive"},
}

STATUS_ALIASES = {
    "initiatives.csv": {"Completed": "Complete"},
    "commitments.csv": {"Complete": "Completed", "In Progress": "Open"},
}

OTHER_ALLOWED_VALUES = {
    "priority": {"Low", "Medium", "High"},
    "severity": {"Low", "Medium", "High"},
    "likelihood": {"Low", "Medium", "High"},
    "threshold_status": {"Healthy", "Good", "Warning", "Critical", "Not Evaluated"},
    "source_authority": {"Working", "Approved", "Official"},
    "escalation_level": {"None", "Manager", "Director"},
}

REFERENCE_COLUMNS = {
    "initiatives.csv": {"program": "program"},
    "commitments.csv": {"initiative": "initiative"},
    "dependencies.csv": {"initiative": "initiative"},
    "risks.csv": {"initiative": "initiative"},
    "knowledge.csv": {"initiative": "initiative_optional"},
    "metric_snapshots.csv": {"initiative": "initiative_optional"},
}


@dataclass
class CsvData:
    path: Path
    headers: list[str]
    rows: list[dict[str, str]]


def template_name_for(sample_name: str) -> str:
    return sample_name.replace(".csv", "_template.csv")


def read_csv(path: Path) -> CsvData:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    return CsvData(path=path, headers=headers, rows=rows)


def read_template_headers(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def is_valid_date(value: str) -> bool:
    if not value:
        return True
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def describe_row(row_index: int) -> str:
    return f"row {row_index + 2}"


def collect_key_values(data_by_file: dict[str, CsvData]) -> tuple[set[str], set[str]]:
    program_values: set[str] = set()
    initiative_values: set[str] = set()

    programs = data_by_file.get("programs.csv")
    if programs:
        for row in programs.rows:
            if row.get("program_id"):
                program_values.add(row["program_id"])
            if row.get("program_name"):
                program_values.add(row["program_name"])

    initiatives = data_by_file.get("initiatives.csv")
    if initiatives:
        for row in initiatives.rows:
            if row.get("initiative_id"):
                initiative_values.add(row["initiative_id"])
            if row.get("initiative_name"):
                initiative_values.add(row["initiative_name"])

    return program_values, initiative_values


def validate_headers(sample: CsvData, template_headers: list[str], errors: list[str], warnings: list[str]) -> None:
    missing = [header for header in template_headers if header not in sample.headers]
    unexpected = [header for header in sample.headers if header not in template_headers]

    if missing:
        errors.append(f"{sample.path.name}: missing required columns: {', '.join(missing)}")
    if unexpected:
        warnings.append(f"{sample.path.name}: unexpected columns: {', '.join(unexpected)}")


def validate_ids(sample: CsvData, errors: list[str]) -> None:
    id_column = ID_COLUMNS.get(sample.path.name)
    if not id_column:
        return

    seen: dict[str, int] = {}
    for row_index, row in enumerate(sample.rows):
        value = row.get(id_column, "")
        if not value:
            errors.append(f"{sample.path.name}: {describe_row(row_index)} missing {id_column}")
            continue
        if value in seen:
            first_row = seen[value] + 2
            errors.append(
                f"{sample.path.name}: {describe_row(row_index)} duplicate {id_column} '{value}' "
                f"first seen on row {first_row}"
            )
        else:
            seen[value] = row_index


def validate_dates(sample: CsvData, errors: list[str]) -> None:
    for row_index, row in enumerate(sample.rows):
        for column in DATE_COLUMNS.get(sample.path.name, []):
            value = row.get(column, "")
            if not is_valid_date(value):
                errors.append(
                    f"{sample.path.name}: {describe_row(row_index)} has invalid {column} '{value}' "
                    "(expected YYYY-MM-DD)"
                )


def validate_statuses(sample: CsvData, errors: list[str], warnings: list[str]) -> None:
    allowed_statuses = STATUS_VALUES.get(sample.path.name)
    status_aliases = STATUS_ALIASES.get(sample.path.name, {})
    if allowed_statuses and "status" in sample.headers:
        for row_index, row in enumerate(sample.rows):
            value = row.get("status", "")
            if not value or value in allowed_statuses:
                continue
            if value in status_aliases:
                warnings.append(
                    f"{sample.path.name}: {describe_row(row_index)} uses status alias '{value}' "
                    f"(normalize to '{status_aliases[value]}' before production load)"
                )
                continue
            allowed = ", ".join(sorted(allowed_statuses))
            errors.append(
                f"{sample.path.name}: {describe_row(row_index)} has invalid status '{value}' "
                f"(allowed: {allowed})"
            )

    for column, allowed_values in OTHER_ALLOWED_VALUES.items():
        if column not in sample.headers:
            continue
        for row_index, row in enumerate(sample.rows):
            value = row.get(column, "")
            if value and value not in allowed_values:
                allowed = ", ".join(sorted(allowed_values))
                errors.append(
                    f"{sample.path.name}: {describe_row(row_index)} has invalid {column} '{value}' "
                    f"(allowed: {allowed})"
                )


def validate_references(
    sample: CsvData,
    program_values: set[str],
    initiative_values: set[str],
    errors: list[str],
) -> None:
    reference_columns = REFERENCE_COLUMNS.get(sample.path.name, {})
    for row_index, row in enumerate(sample.rows):
        for column, reference_type in reference_columns.items():
            value = row.get(column, "")
            if not value and reference_type.endswith("_optional"):
                continue
            if not value:
                errors.append(f"{sample.path.name}: {describe_row(row_index)} missing {column} reference")
                continue

            if reference_type == "program" and value not in program_values:
                errors.append(
                    f"{sample.path.name}: {describe_row(row_index)} references unknown program '{value}'"
                )
            elif reference_type.startswith("initiative") and value not in initiative_values:
                errors.append(
                    f"{sample.path.name}: {describe_row(row_index)} references unknown initiative '{value}'"
                )


def validate_directory(input_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not input_dir.exists():
        return [f"Missing input directory: {input_dir}"], warnings
    if not TEMPLATE_DIR.exists():
        return [f"Missing template directory: {TEMPLATE_DIR}"], warnings

    sample_paths = sorted(input_dir.glob("*.csv"))
    if not sample_paths:
        return [f"No CSV files found in {input_dir}"], warnings

    data_by_file = {path.name: read_csv(path) for path in sample_paths}
    program_values, initiative_values = collect_key_values(data_by_file)

    for sample in data_by_file.values():
        template_path = TEMPLATE_DIR / template_name_for(sample.path.name)
        if not template_path.exists():
            errors.append(f"{sample.path.name}: missing template {template_path.name}")
            continue

        template_headers = read_template_headers(template_path)
        validate_headers(sample, template_headers, errors, warnings)
        validate_ids(sample, errors)
        validate_dates(sample, errors)
        validate_statuses(sample, errors, warnings)
        validate_references(sample, program_values, initiative_values, errors)

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate FCC CSV files against templates and core model rules.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing FCC CSV files to validate. Defaults to data/sample.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    errors, warnings = validate_directory(input_dir)

    print(f"Validating FCC CSVs in {input_dir}")
    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        print("FCC CSV validation failed:")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("FCC CSV validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
