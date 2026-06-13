#!/usr/bin/env python3
"""Generate FCC operational overlay CSVs from synthetic RE NXT-style source data.

The generator intentionally does not create FCC-owned activity records. RE NXT
Actions are consumed only as source data for commitments, risks, and metrics.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIRS = [
    REPO_ROOT / "data" / "source",
    REPO_ROOT / "data" / "renxt",
    REPO_ROOT / "data" / "synthetic",
    REPO_ROOT / "data" / "sample_source",
]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "operational_overlay"
TODAY = date(2026, 6, 13)

OUTPUT_FIELDS = {
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
        "source",
        "notes",
    ],
}

INITIATIVES = {
    "annual_giving": {
        "initiative_id": "INI-AG-SPRING",
        "initiative_name": "Spring Appeal",
        "program": "PRG-AG",
        "initiative_type": "Appeal",
        "owner": "Annual Giving Manager",
        "department": "Annual Giving",
        "status": "Active",
        "start_date": "2026-03-01",
        "target_date": "2026-06-30",
        "goal_amount": "250000",
        "source_system": "RE NXT",
        "source_record_id": "APPEAL-2026-SPRING",
    },
    "major_gifts": {
        "initiative_id": "INI-MG-PGP",
        "initiative_name": "Principal Gifts Portfolio",
        "program": "PRG-MG",
        "initiative_type": "Portfolio",
        "owner": "Principal Gifts Director",
        "department": "Major Gifts",
        "status": "Active",
        "start_date": "2026-01-15",
        "target_date": "2026-12-31",
        "goal_amount": "5000000",
        "source_system": "RE NXT",
        "source_record_id": "PORTFOLIO-PRINCIPAL-2026",
    },
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
        normalized = normalize_header(name)
        if row.get(normalized):
            return row[normalized]
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


def classify_initiative(row: dict[str, str]) -> str:
    text = " ".join(row.values()).lower()
    amount = parse_amount(first_present(row, ["amount", "ask_amount", "opportunity_amount", "expected_amount", "value"]))
    if "spring" in text or "annual" in text or "appeal" in text or amount < 100000:
        return "annual_giving"
    return "major_gifts"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [normalize_row(row) for row in csv.DictReader(handle)]


def discover_source_files(input_dir: Path) -> SourceData:
    opportunities: list[dict[str, str]] = []
    actions: list[dict[str, str]] = []
    appeals: list[dict[str, str]] = []

    if not input_dir.exists():
        return SourceData(opportunities=opportunities, actions=actions, appeals=appeals)

    for path in sorted(input_dir.glob("*.csv")):
        name = path.name.lower()
        rows = read_csv(path)
        if "opportun" in name or "proposal" in name:
            opportunities.extend(rows)
        elif "action" in name or "activity" in name or "task" in name:
            actions.extend(rows)
        elif "appeal" in name or "campaign" in name:
            appeals.extend(rows)

    return SourceData(opportunities=opportunities, actions=actions, appeals=appeals)


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
                "action_type": "Call",
                "status": "Not Completed",
                "owner": "Development Officer",
                "due_date": "2026-06-10",
                "completed_date": "",
            },
            {
                "action_id": "ACT-MG-2026-091",
                "opportunity_id": "OPP-MG-2026-001",
                "action_type": "Strategy Discussion",
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


def generate_initiatives(source: SourceData) -> list[dict[str, str]]:
    initiatives = {key: value.copy() for key, value in INITIATIVES.items()}

    annual_goal = 0.0
    for appeal in source.appeals:
        text = " ".join(appeal.values()).lower()
        if "spring" in text or "annual" in text:
            annual_goal += parse_amount(first_present(appeal, ["goal_amount", "goal", "target", "amount"]))
            appeal_id = source_id(appeal, "APPEAL", 0)
            initiatives["annual_giving"]["source_record_id"] = appeal_id

    if annual_goal > 0:
        initiatives["annual_giving"]["goal_amount"] = str(int(annual_goal))

    major_goal = sum(
        parse_amount(first_present(row, ["amount", "ask_amount", "opportunity_amount", "expected_amount", "value"]))
        for row in source.opportunities
        if classify_initiative(row) == "major_gifts"
    )
    if major_goal > 0:
        initiatives["major_gifts"]["goal_amount"] = str(int(major_goal))

    return list(initiatives.values())


def generate_commitments(source: SourceData) -> list[dict[str, str]]:
    commitments: list[dict[str, str]] = []

    for index, row in enumerate(source.opportunities):
        initiative_key = classify_initiative(row)
        initiative = INITIATIVES[initiative_key]["initiative_id"]
        amount = parse_amount(first_present(row, ["amount", "ask_amount", "opportunity_amount", "expected_amount", "value"]))
        due = parse_date(first_present(row, ["expected_date", "ask_date", "proposal_due_date", "target_date", "close_date"]))
        status = first_present(row, ["status", "opportunity_status", "stage"], "Open")
        completed = is_completed(status)
        commitment_status = "Completed" if completed else "Overdue" if due and due < TODAY else "Open"
        source_record_id = source_id(row, "OPP", index)
        commitment_type = "Proposal" if amount >= 100000 else "Donor Follow-Up"
        owner = owner_from(row, "Major Gifts Officer" if initiative_key == "major_gifts" else "Development Officer")

        commitments.append(
            {
                "commitment_id": f"COM-OPP-{slug(source_record_id)}",
                "commitment_name": first_present(
                    row,
                    ["opportunity_name", "name", "description"],
                    "Advance fundraising opportunity",
                ),
                "initiative": initiative,
                "commitment_type": commitment_type,
                "owner": owner,
                "due_date": format_date(due or TODAY + timedelta(days=14)),
                "status": commitment_status,
                "priority": "High" if amount >= 1000000 else "Medium",
                "value_amount": str(int(amount)) if amount else "0",
                "source_system": "RE NXT",
                "source_record_id": source_record_id,
                "escalation_level": "Manager" if commitment_status == "Overdue" else "None",
                "notes": "Generated from RE NXT-style opportunity source data.",
            }
        )

    for index, row in enumerate(source.actions):
        initiative_key = classify_initiative(row)
        initiative = INITIATIVES[initiative_key]["initiative_id"]
        due = parse_date(first_present(row, ["due_date", "date", "action_date", "scheduled_date"]))
        completed = is_completed(first_present(row, ["status", "action_status", "completed"], ""))
        action_type = first_present(row, ["action_type", "type", "category"], "Follow-Up")
        source_record_id = source_id(row, "ACT", index)
        owner = owner_from(row, "Major Gifts Officer" if initiative_key == "major_gifts" else "Development Officer")

        commitments.append(
            {
                "commitment_id": f"COM-ACT-{slug(source_record_id)}",
                "commitment_name": f"Complete {action_type.lower()} follow-up",
                "initiative": initiative,
                "commitment_type": "Donor Follow-Up",
                "owner": owner,
                "due_date": format_date(due or TODAY + timedelta(days=7)),
                "status": "Completed" if completed else "Overdue" if due and due < TODAY else "Open",
                "priority": "High" if initiative_key == "major_gifts" else "Medium",
                "value_amount": "0",
                "source_system": "RE NXT Actions",
                "source_record_id": source_record_id,
                "escalation_level": "Manager" if due and due < TODAY and not completed else "None",
                "notes": "RE NXT Actions remain source data; FCC tracks the resulting commitment only.",
            }
        )

    return dedupe_by_id(commitments, "commitment_id")


def generate_dependencies(source: SourceData) -> list[dict[str, str]]:
    has_major = any(classify_initiative(row) == "major_gifts" for row in source.opportunities)
    has_annual = bool(source.appeals) or any(classify_initiative(row) == "annual_giving" for row in source.opportunities + source.actions)

    dependencies: list[dict[str, str]] = []
    if has_annual:
        dependencies.extend(
            [
                {
                    "dependency_id": "DEP-AG-FINANCE-CODING",
                    "dependency_name": "Finance coding approval for appeal response tracking",
                    "initiative": "INI-AG-SPRING",
                    "dependency_type": "Approval",
                    "blocking_area": "Finance",
                    "impacted_area": "Annual Giving",
                    "owner": "Finance Business Partner",
                    "due_date": format_date(TODAY - timedelta(days=6)),
                    "status": "Open",
                    "severity": "High",
                    "impact_description": "Appeal response reporting cannot be finalized until coding is approved.",
                    "resolution_notes": "",
                },
                {
                    "dependency_id": "DEP-AG-CREATIVE-APPROVAL",
                    "dependency_name": "Email creative final approval",
                    "initiative": "INI-AG-SPRING",
                    "dependency_type": "Review",
                    "blocking_area": "Marketing",
                    "impacted_area": "Annual Giving",
                    "owner": "Marketing Lead",
                    "due_date": format_date(TODAY + timedelta(days=1)),
                    "status": "Open",
                    "severity": "Medium",
                    "impact_description": "Final email deployment is waiting for creative approval.",
                    "resolution_notes": "",
                },
            ]
        )

    if has_major:
        dependencies.extend(
            [
                {
                    "dependency_id": "DEP-MG-RESEARCH-REFRESH",
                    "dependency_name": "Prospect research refresh for principal gift briefing",
                    "initiative": "INI-MG-PGP",
                    "dependency_type": "Resource",
                    "blocking_area": "Prospect Research",
                    "impacted_area": "Major Gifts",
                    "owner": "Prospect Research Manager",
                    "due_date": format_date(TODAY - timedelta(days=8)),
                    "status": "Open",
                    "severity": "High",
                    "impact_description": "Executive briefing is blocked until updated capacity and affinity notes are available.",
                    "resolution_notes": "",
                },
                {
                    "dependency_id": "DEP-MG-CASE-APPROVAL",
                    "dependency_name": "Case for support approval",
                    "initiative": "INI-MG-PGP",
                    "dependency_type": "Approval",
                    "blocking_area": "Leadership",
                    "impacted_area": "Major Gifts",
                    "owner": "VP Development",
                    "due_date": format_date(TODAY + timedelta(days=7)),
                    "status": "Open",
                    "severity": "High",
                    "impact_description": "Proposal development is blocked until leadership approves the case language.",
                    "resolution_notes": "",
                },
            ]
        )

    return dependencies


def generate_risks(source: SourceData, commitments: list[dict[str, str]], dependencies: list[dict[str, str]]) -> list[dict[str, str]]:
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
        due = parse_date(dependency["due_date"])
        if dependency["severity"] == "High" and dependency["status"] != "Resolved":
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

    future_actions_by_opportunity = defaultdict(int)
    completed_actions_by_opportunity: dict[str, date] = {}
    for action in source.actions:
        opportunity_id = first_present(action, ["opportunity_id", "opportunity_lookup_id", "linked_opportunity_id"])
        due = parse_date(first_present(action, ["due_date", "date", "action_date", "scheduled_date"]))
        completed_date = parse_date(first_present(action, ["completed_date", "date_completed", "completion_date"]))
        if opportunity_id and due and due >= TODAY:
            future_actions_by_opportunity[opportunity_id] += 1
        if opportunity_id and completed_date:
            previous = completed_actions_by_opportunity.get(opportunity_id)
            completed_actions_by_opportunity[opportunity_id] = max(previous, completed_date) if previous else completed_date

    for index, opportunity in enumerate(source.opportunities):
        opportunity_id = source_id(opportunity, "OPP", index)
        initiative = INITIATIVES[classify_initiative(opportunity)]["initiative_id"]
        amount = parse_amount(first_present(opportunity, ["amount", "ask_amount", "opportunity_amount", "expected_amount", "value"]))
        owner = owner_from(opportunity, "Major Gifts Officer")
        last_completed = completed_actions_by_opportunity.get(opportunity_id)
        missing_next_action = future_actions_by_opportunity[opportunity_id] == 0
        stalled = not last_completed or last_completed < TODAY - timedelta(days=90)

        if missing_next_action:
            risks.append(
                {
                    "risk_id": f"RSK-MISSING-NEXT-ACTION-{slug(opportunity_id)}",
                    "risk_name": "Missing next action for active opportunity",
                    "initiative": initiative,
                    "risk_type": "Follow-Up",
                    "severity": "High" if amount >= 1000000 else "Medium",
                    "likelihood": "High",
                    "status": "Open",
                    "owner": owner,
                    "date_identified": format_date(TODAY),
                    "target_resolution_date": format_date(TODAY + timedelta(days=7)),
                    "source_system": "RE NXT Actions",
                    "source_record_id": opportunity_id,
                    "mitigation_plan": "Create or confirm the next relationship action in RE NXT.",
                }
            )

        if stalled and amount >= 100000:
            risks.append(
                {
                    "risk_id": f"RSK-STALLED-{slug(opportunity_id)}",
                    "risk_name": "Stalled fundraising opportunity",
                    "initiative": initiative,
                    "risk_type": "Pipeline",
                    "severity": "High" if amount >= 1000000 else "Medium",
                    "likelihood": "Medium",
                    "status": "Open",
                    "owner": owner,
                    "date_identified": format_date(TODAY),
                    "target_resolution_date": format_date(TODAY + timedelta(days=14)),
                    "source_system": "RE NXT",
                    "source_record_id": opportunity_id,
                    "mitigation_plan": "Review opportunity strategy and confirm recent meaningful contact.",
                }
            )

    return dedupe_by_id(risks, "risk_id")


def generate_knowledge() -> list[dict[str, str]]:
    return [
        {
            "knowledge_id": "KNW-AG-SPRING-SEGMENTATION-SOP",
            "title": "Spring Appeal Segmentation SOP",
            "knowledge_type": "SOP",
            "initiative": "INI-AG-SPRING",
            "owner": "Annual Giving Manager",
            "status": "Approved",
            "source_authority": "Official",
            "review_date": "2026-09-30",
            "document_link": "https://sharepoint.example.com/sites/fcc/knowledge/spring-appeal-segmentation-sop",
            "tags": "annual-giving;segmentation;appeal",
        },
        {
            "knowledge_id": "KNW-MG-BRIEFING-TEMPLATE",
            "title": "Principal Gift Briefing Template",
            "knowledge_type": "Template",
            "initiative": "INI-MG-PGP",
            "owner": "Principal Gifts Director",
            "status": "Approved",
            "source_authority": "Official",
            "review_date": "2026-10-31",
            "document_link": "https://sharepoint.example.com/sites/fcc/knowledge/principal-gift-briefing-template",
            "tags": "major-gifts;briefing;template",
        },
    ]


def threshold_status(value: int, metric_name: str) -> str:
    if metric_name == "Readiness Score":
        if value < 65:
            return "Critical"
        if value < 80:
            return "Warning"
        return "Healthy"
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
        initiative_dependencies = [row for row in dependencies if row["initiative"] == initiative_id and row["status"] != "Resolved"]
        initiative_risks = [row for row in risks if row["initiative"] == initiative_id and row["status"] != "Resolved"]
        overdue_commitments = [row for row in initiative_commitments if row["status"] == "Overdue"]
        completed_commitments = [row for row in initiative_commitments if row["status"] == "Completed"]

        readiness = max(
            35,
            90 - (len(overdue_commitments) * 8) - (len(initiative_dependencies) * 7) - (len([r for r in initiative_risks if r["severity"] == "High"]) * 10),
        )
        follow_up_total = len([row for row in initiative_commitments if row["commitment_type"] == "Donor Follow-Up"])
        follow_up_completed = len(
            [row for row in initiative_commitments if row["commitment_type"] == "Donor Follow-Up" and row["status"] == "Completed"]
        )
        follow_up_compliance = round((follow_up_completed / follow_up_total) * 100) if follow_up_total else 100

        metrics = [
            ("Readiness Score", readiness, "Score", f"Readiness generated from overdue commitments, open dependencies, and high risks for {initiative['initiative_name']}."),
            ("Open Risks", len(initiative_risks), "Count", "Open risks generated by the FCC rules layer."),
            ("Overdue Commitments", len(overdue_commitments), "Count", "Overdue commitments derived from FCC commitment due dates."),
            ("Open Dependencies", len(initiative_dependencies), "Count", "Open blockers and prerequisites for the initiative."),
            ("Follow-Up Compliance", follow_up_compliance, "Percent", "Uses RE NXT Actions only as source activity data."),
        ]

        for metric_name, metric_value, unit, notes in metrics:
            snapshots.append(
                {
                    "snapshot_id": f"SNP-{slug(initiative_id)}-{slug(metric_name)}-{TODAY.isoformat()}",
                    "snapshot_date": format_date(TODAY),
                    "initiative": initiative_id,
                    "metric_name": metric_name,
                    "metric_value": str(metric_value),
                    "metric_unit": unit,
                    "threshold_status": threshold_status(int(metric_value), metric_name),
                    "source": "Power Automate",
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


def generate_overlay(input_dir: Path, output_dir: Path) -> None:
    source = load_source_data(input_dir)
    initiatives = generate_initiatives(source)
    commitments = generate_commitments(source)
    dependencies = generate_dependencies(source)
    risks = generate_risks(source, commitments, dependencies)
    knowledge = generate_knowledge()
    metric_snapshots = generate_metric_snapshots(initiatives, commitments, dependencies, risks)

    outputs = {
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate_overlay(args.input_dir.resolve(), args.output_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
