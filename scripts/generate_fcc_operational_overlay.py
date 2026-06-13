#!/usr/bin/env python3
"""Generate FCC operational overlay CSVs from synthetic RE NXT-style source data.

The generator intentionally does not create FCC-owned activity records. RE NXT
Actions are consumed only as source data for commitments, risks, and metrics.
Mapping assumptions are read from config/fcc_mapping_config.json so they remain
explicit implementation choices rather than hidden canonical model rules.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "fcc_mapping_config.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "operational_overlay"
DEFAULT_INPUT_DIRS = [
    REPO_ROOT / "data" / "source",
    REPO_ROOT / "data" / "renxt",
    REPO_ROOT / "data" / "synthetic",
    REPO_ROOT / "data" / "sample_source",
]
TODAY = date(2026, 6, 13)

OUTPUT_FIELDS = {
    "programs.csv": [
        "program_id",
        "program_name",
        "program_type",
        "executive_owner",
        "department",
        "status",
        "strategic_goal",
        "start_date",
        "end_date",
    ],
    "initiatives.csv": [
        "initiative_id",
        "initiative_name",
        "program",
        "initiative_type",
        "owner",
        "department",
        "status",
        "start_date",
        "target_date",
        "goal_amount",
        "readiness_score",
        "risk_score",
        "source_system",
        "source_record_id",
    ],
    "commitments.csv": [
        "commitment_id",
        "commitment_name",
        "initiative",
        "commitment_type",
        "owner",
        "due_date",
        "status",
        "priority",
        "value_amount",
        "source_system",
        "source_record_id",
        "escalation_level",
        "notes",
    ],
    "dependencies.csv": [
        "dependency_id",
        "dependency_name",
        "initiative",
        "dependency_type",
        "blocking_area",
        "impacted_area",
        "owner",
        "due_date",
        "status",
        "severity",
        "impact_description",
        "resolution_notes",
    ],
    "risks.csv": [
        "risk_id",
        "risk_name",
        "initiative",
        "risk_type",
        "severity",
        "likelihood",
        "status",
        "owner",
        "date_identified",
        "target_resolution_date",
        "source_system",
        "source_record_id",
        "mitigation_plan",
    ],
    "knowledge.csv": [
        "knowledge_id",
        "title",
        "knowledge_type",
        "initiative",
        "owner",
        "status",
        "source_authority",
        "review_date",
        "document_link",
        "tags",
    ],
    "metric_snapshots.csv": [
        "snapshot_id",
        "snapshot_date",
        "initiative",
        "metric_name",
        "metric_value",
        "metric_unit",
        "threshold_status",
        "source_system",
        "notes",
    ],
}


@dataclass
class SourceData:
    opportunities: list[dict[str, str]]
    actions: list[dict[str, str]]
    appeals: list[dict[str, str]]


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {normalize_header(key): (value or "").strip() for key, value in row.items()}


def first_present(row: dict[str, str], names: Iterable[str], default: str = "") -> str:
    for name in names:
        value = row.get(normalize_header(name), "")
        if value:
            return value
    return default


def parse_amount(value: str) -> float:
    cleaned = re.sub(r"[^0-9.-]", "", value or "")
    try:
        return float(cleaned) if cleaned else 0.0
    except ValueError:
        return 0.0


def parse_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d/%m/%Y", "%b %d %Y", "%B %d %Y"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            pass
    return None


def format_date(value: date | None) -> str:
    return value.isoformat() if value else ""


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.upper()).strip("-")
    return cleaned[:40] or "UNKNOWN"


def source_id(row: dict[str, str], fallback_prefix: str, index: int) -> str:
    return first_present(
        row,
        [
            "opportunity_id",
            "opportunity_lookup_id",
            "action_id",
            "action_lookup_id",
            "appeal_id",
            "campaign_id",
            "id",
            "record_id",
            "system_record_id",
        ],
        f"{fallback_prefix}-{index + 1:03d}",
    )


def owner_from(row: dict[str, str], default: str) -> str:
    return first_present(
        row,
        ["owner", "assigned_to", "assigned_fundraiser", "fundraiser", "solicitor", "primary_manager"],
        default,
    )


def is_completed(value: str) -> bool:
    return value.strip().lower() in {"complete", "completed", "closed", "done"}


def load_mapping_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [normalize_row(row) for row in csv.DictReader(handle)]


def discover_source_files(input_dir: Path) -> SourceData:
    source = SourceData(opportunities=[], actions=[], appeals=[])
    if not input_dir.exists():
        return source

    for path in sorted(input_dir.glob("*.csv")):
        name = path.name.lower()
        rows = read_csv(path)
        if "opportun" in name or "proposal" in name:
            source.opportunities.extend(rows)
        elif "action" in name or "activity" in name or "task" in name:
            source.actions.extend(rows)
        elif "appeal" in name or "campaign" in name:
            source.appeals.extend(rows)
    return source


def fallback_source_data() -> SourceData:
    return SourceData(
        opportunities=[
            {
                "opportunity_id": "OPP-MG-2026-001",
                "opportunity_name": "Principal gift proposal readiness",
                "amount": "2500000",
                "status": "Active",
                "stage": "Proposal Development",
                "owner": "Major Gifts Officer",
                "expected_date": "2026-06-28",
            },
            {
                "opportunity_id": "OPP-AG-2026-001",
                "opportunity_name": "Spring Appeal leadership donor follow-up",
                "amount": "15000",
                "status": "Active",
                "stage": "Cultivation",
                "owner": "Development Officer",
                "expected_date": "2026-06-10",
            },
        ],
        actions=[
            {
                "action_id": "ACT-AG-2026-044",
                "opportunity_id": "OPP-AG-2026-001",
                "action_type": "Spring Appeal follow-up call",
                "status": "Not Completed",
                "owner": "Development Officer",
                "due_date": "2026-06-10",
                "completed_date": "",
            },
            {
                "action_id": "ACT-MG-2026-091",
                "opportunity_id": "OPP-MG-2026-001",
                "action_type": "Principal gift strategy discussion",
                "status": "Open",
                "owner": "Major Gifts Officer",
                "due_date": "2026-06-17",
                "completed_date": "",
            },
        ],
        appeals=[
            {
                "appeal_id": "APPEAL-2026-SPRING",
                "appeal_name": "Spring Appeal",
                "goal_amount": "250000",
                "owner": "Annual Giving Manager",
            }
        ],
    )


def load_source_data(input_dir: Path) -> SourceData:
    source = discover_source_files(input_dir)
    if source.opportunities or source.actions or source.appeals:
        return source
    return fallback_source_data()


def initiatives_by_key(config: dict) -> dict[str, dict[str, str]]:
    return {initiative["initiative_key"]: initiative for initiative in config.get("initiatives", [])}


def match_initiative_key(row: dict[str, str], config: dict, source_type: str) -> str | None:
    fallback_key: str | None = None
    for initiative in config.get("initiatives", []):
        if initiative.get("fallback_for_unmatched_opportunities") and source_type == "opportunity":
            fallback_key = initiative["initiative_key"]

        match = initiative.get("source_match", {})
        fields = [normalize_header(field) for field in match.get("fields", [])]
        needles = [str(value).lower() for value in match.get("contains_any", [])]
        haystack = " ".join(row.get(field, "") for field in fields).lower()
        if needles and any(needle in haystack for needle in needles):
            return initiative["initiative_key"]
    return fallback_key


def generate_programs(config: dict) -> list[dict[str, str]]:
    return [program.copy() for program in config.get("programs", [])]


def generate_initiatives(source: SourceData, config: dict) -> list[dict[str, str]]:
    initiatives = []
    for configured in config.get("initiatives", []):
        row = configured.copy()
        row.pop("initiative_key", None)
        row.pop("source_match", None)
        row.pop("fallback_for_unmatched_opportunities", None)
        initiatives.append(row)

    configured_by_key = initiatives_by_key(config)
    for appeal in source.appeals:
        initiative_key = match_initiative_key(appeal, config, "appeal")
        if not initiative_key:
            continue
        target_id = configured_by_key[initiative_key]["initiative_id"]
        for initiative in initiatives:
            if initiative["initiative_id"] != target_id:
                continue
            goal = parse_amount(first_present(appeal, ["goal_amount", "goal", "target", "amount"]))
            if goal:
                initiative["goal_amount"] = str(int(goal))
            initiative["source_record_id"] = source_id(appeal, "APPEAL", 0)
    return initiatives


def generate_commitments(source: SourceData, config: dict) -> list[dict[str, str]]:
    commitments: list[dict[str, str]] = []
    initiative_lookup = initiatives_by_key(config)
    mappings = config.get("source_mappings", {})
    high_value_amount = parse_amount(str(config.get("thresholds", {}).get("high_value_amount", 1000000)))

    opportunity_mapping = mappings.get("opportunities", {})
    if opportunity_mapping.get("enabled") and opportunity_mapping.get("create_commitments"):
        for index, row in enumerate(source.opportunities):
            initiative_key = match_initiative_key(row, config, "opportunity")
            if not initiative_key:
                continue
            initiative = initiative_lookup[initiative_key]
            amount = parse_amount(first_present(row, ["amount", "ask_amount", "opportunity_amount", "expected_amount", "value"]))
            due = parse_date(first_present(row, ["expected_date", "ask_date", "proposal_due_date", "target_date", "close_date"]))
            status = first_present(row, ["status", "opportunity_status", "stage"], "Open")
            commitment_status = "Completed" if is_completed(status) else "Overdue" if due and due < TODAY else "Open"
            source_record_id = source_id(row, "OPP", index)

            commitments.append(
                {
                    "commitment_id": f"COM-OPP-{slug(source_record_id)}",
                    "commitment_name": first_present(row, ["opportunity_name", "name", "description"], "Advance mapped fundraising opportunity"),
                    "initiative": initiative["initiative_id"],
                    "commitment_type": opportunity_mapping.get("commitment_type", "Proposal"),
                    "owner": owner_from(row, initiative.get("owner", "Development Officer")),
                    "due_date": format_date(due or TODAY + timedelta(days=14)),
                    "status": commitment_status,
                    "priority": "High" if amount >= high_value_amount else "Medium",
                    "value_amount": str(int(amount)) if amount else "0",
                    "source_system": "RE NXT",
                    "source_record_id": source_record_id,
                    "escalation_level": "Manager" if commitment_status == "Overdue" else "None",
                    "notes": "Generated from an explicit opportunity-to-commitment mapping in config/fcc_mapping_config.json.",
                }
            )

    action_mapping = mappings.get("actions", {})
    if action_mapping.get("enabled") and action_mapping.get("create_follow_up_commitments"):
        for index, row in enumerate(source.actions):
            initiative_key = match_initiative_key(row, config, "action")
            if not initiative_key:
                continue
            initiative = initiative_lookup[initiative_key]
            due = parse_date(first_present(row, ["due_date", "date", "action_date", "scheduled_date"]))
            completed = is_completed(first_present(row, ["status", "action_status", "completed"], ""))
            source_record_id = source_id(row, "ACT", index)
            action_type = first_present(row, ["action_type", "type", "category"], "Follow-Up")

            commitments.append(
                {
                    "commitment_id": f"COM-ACT-{slug(source_record_id)}",
                    "commitment_name": f"Complete {action_type.lower()} follow-up",
                    "initiative": initiative["initiative_id"],
                    "commitment_type": action_mapping.get("commitment_type", "Donor Follow-Up"),
                    "owner": owner_from(row, initiative.get("owner", "Development Officer")),
                    "due_date": format_date(due or TODAY + timedelta(days=7)),
                    "status": "Completed" if completed else "Overdue" if due and due < TODAY else "Open",
                    "priority": "Medium",
                    "value_amount": "0",
                    "source_system": "RE NXT Actions",
                    "source_record_id": source_record_id,
                    "escalation_level": "Manager" if due and due < TODAY and not completed else "None",
                    "notes": "RE NXT Actions remain source activity data; FCC tracks the resulting commitment only.",
                }
            )

    return dedupe_by_id(commitments, "commitment_id")


def generate_dependencies(config: dict) -> list[dict[str, str]]:
    dependencies: list[dict[str, str]] = []
    for dependency in config.get("default_dependencies", []):
        row = dependency.copy()
        offset = int(row.pop("due_date_offset_days", 0))
        row["due_date"] = format_date(TODAY + timedelta(days=offset))
        dependencies.append(row)
    return dependencies


def generate_risks(commitments: list[dict[str, str]], dependencies: list[dict[str, str]]) -> list[dict[str, str]]:
    risks: list[dict[str, str]] = []
    for commitment in commitments:
        if commitment["status"] != "Overdue":
            continue
        risks.append(
            {
                "risk_id": f"RSK-{commitment['commitment_id']}",
                "risk_name": f"Overdue commitment: {commitment['commitment_name']}",
                "initiative": commitment["initiative"],
                "risk_type": "Follow-Up" if commitment["commitment_type"] == "Donor Follow-Up" else "Commitment",
                "severity": "High" if commitment["priority"] == "High" else "Medium",
                "likelihood": "High",
                "status": "Open",
                "owner": commitment["owner"],
                "date_identified": format_date(TODAY),
                "target_resolution_date": format_date(TODAY + timedelta(days=7)),
                "source_system": commitment["source_system"],
                "source_record_id": commitment["source_record_id"],
                "mitigation_plan": "Confirm owner action plan and resolve overdue commitment before the next review cycle.",
            }
        )

    for dependency in dependencies:
        if dependency["severity"] != "High" or dependency["status"] == "Resolved":
            continue
        due = parse_date(dependency["due_date"])
        risks.append(
            {
                "risk_id": f"RSK-{dependency['dependency_id']}",
                "risk_name": f"Blocked dependency: {dependency['dependency_name']}",
                "initiative": dependency["initiative"],
                "risk_type": "Dependency",
                "severity": "High",
                "likelihood": "High" if due and due < TODAY else "Medium",
                "status": "Open",
                "owner": dependency["owner"],
                "date_identified": format_date(TODAY),
                "target_resolution_date": format_date(TODAY + timedelta(days=10)),
                "source_system": "Power Automate",
                "source_record_id": dependency["dependency_id"],
                "mitigation_plan": "Escalate blocker and confirm an owner-backed resolution date.",
            }
        )

    return dedupe_by_id(risks, "risk_id")


def generate_knowledge(config: dict) -> list[dict[str, str]]:
    return [asset.copy() for asset in config.get("knowledge_assets", [])]


def threshold_status_for_count(value: int) -> str:
    if value >= 2:
        return "Critical"
    if value == 1:
        return "Warning"
    return "Healthy"


def generate_metric_snapshots(
    initiatives: list[dict[str, str]],
    commitments: list[dict[str, str]],
    dependencies: list[dict[str, str]],
    risks: list[dict[str, str]],
) -> list[dict[str, str]]:
    snapshots: list[dict[str, str]] = []
    for initiative in initiatives:
        initiative_id = initiative["initiative_id"]
        initiative_commitments = [row for row in commitments if row["initiative"] == initiative_id]
        open_commitments = [row for row in initiative_commitments if row["status"] != "Completed"]
        overdue_commitments = [row for row in initiative_commitments if row["status"] == "Overdue"]
        open_dependencies = [row for row in dependencies if row["initiative"] == initiative_id and row["status"] != "Resolved"]
        open_risks = [row for row in risks if row["initiative"] == initiative_id and row["status"] != "Resolved"]
        high_risks = [row for row in open_risks if row["severity"] == "High"]

        metrics = [
            (
                "open_commitments_count",
                str(len(open_commitments)),
                "Count",
                threshold_status_for_count(len(open_commitments)),
                "Simple count of FCC commitments that are not completed.",
            ),
            (
                "overdue_commitments_count",
                str(len(overdue_commitments)),
                "Count",
                threshold_status_for_count(len(overdue_commitments)),
                "Simple count of FCC commitments with overdue status.",
            ),
            (
                "open_dependencies_count",
                str(len(open_dependencies)),
                "Count",
                threshold_status_for_count(len(open_dependencies)),
                "Simple count of open FCC dependencies.",
            ),
            (
                "high_risks_count",
                str(len(high_risks)),
                "Count",
                threshold_status_for_count(len(high_risks)),
                "Simple count of open high-severity FCC risks.",
            ),
            (
                "commitment_compliance",
                "",
                "Percent",
                "Not Evaluated",
                "Placeholder/config_input only. No weighted commitment compliance formula is calculated in the MVP overlay.",
            ),
            (
                "follow_up_compliance",
                "",
                "Percent",
                "Not Evaluated",
                "Placeholder/config_input only. RE NXT Actions remain source activity data; no compliance formula is calculated in the MVP overlay.",
            ),
            (
                "readiness_score_placeholder",
                initiative.get("readiness_score", ""),
                "Score",
                "Not Evaluated",
                "Placeholder/config_input only. Imported Initiative score; no readiness formula is calculated.",
            ),
            (
                "risk_score_placeholder",
                initiative.get("risk_score", ""),
                "Score",
                "Not Evaluated",
                "Placeholder/config_input only. Imported Initiative score; no risk formula is calculated.",
            ),
        ]

        for metric_name, metric_value, unit, threshold_status, notes in metrics:
            snapshots.append(
                {
                    "snapshot_id": f"SNP-{slug(initiative_id)}-{slug(metric_name)}-{TODAY.isoformat()}",
                    "snapshot_date": format_date(TODAY),
                    "initiative": initiative_id,
                    "metric_name": metric_name,
                    "metric_value": metric_value,
                    "metric_unit": unit,
                    "threshold_status": threshold_status,
                    "source_system": "Power Automate",
                    "notes": notes,
                }
            )
    return snapshots


def dedupe_by_id(rows: list[dict[str, str]], id_column: str) -> list[dict[str, str]]:
    deduped: dict[str, dict[str, str]] = {}
    for row in rows:
        deduped[row[id_column]] = row
    return list(deduped.values())


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def generate_overlay(input_dir: Path, output_dir: Path, config_path: Path) -> None:
    config = load_mapping_config(config_path)
    source = load_source_data(input_dir)
    programs = generate_programs(config)
    initiatives = generate_initiatives(source, config)
    commitments = generate_commitments(source, config)
    dependencies = generate_dependencies(config)
    risks = generate_risks(commitments, dependencies)
    knowledge = generate_knowledge(config)
    metric_snapshots = generate_metric_snapshots(initiatives, commitments, dependencies, risks)

    outputs = {
        "programs.csv": programs,
        "initiatives.csv": initiatives,
        "commitments.csv": commitments,
        "dependencies.csv": dependencies,
        "risks.csv": risks,
        "knowledge.csv": knowledge,
        "metric_snapshots.csv": metric_snapshots,
    }

    for filename, rows in outputs.items():
        write_csv(output_dir / filename, OUTPUT_FIELDS[filename], rows)

    print(f"Generated FCC operational overlay in {output_dir}")
    print(f"Mapping config: {config_path}")
    print(f"Source records: {len(source.opportunities)} opportunities, {len(source.actions)} RE NXT actions, {len(source.appeals)} appeals/campaigns")
    for filename, rows in outputs.items():
        print(f"- {filename}: {len(rows)} rows")


def default_input_dir() -> Path:
    for input_dir in DEFAULT_INPUT_DIRS:
        if input_dir.exists() and any(input_dir.glob("*.csv")):
            return input_dir
    return DEFAULT_INPUT_DIRS[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate FCC operational overlay CSVs from RE NXT-style source data.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=default_input_dir(),
        help="Directory containing synthetic RE NXT-style CSV exports. Defaults to the first populated known source directory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where FCC overlay CSVs will be written.",
    )
    parser.add_argument(
        "--mapping-config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="JSON file documenting FCC mapping assumptions.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate_overlay(args.input_dir.resolve(), args.output_dir.resolve(), args.mapping_config.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
