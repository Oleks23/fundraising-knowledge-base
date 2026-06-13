# SharePoint Provisioning Plan

# Fundraising Command Centre (FCC)

Version: 1.1

---

# Purpose

This plan describes how the CSV templates in `data/templates/` map to SharePoint Lists for the Microsoft 365 MVP.

It aligns with `docs/SHAREPOINT_LISTS_DESIGN.md` and preserves the core FCC design principle:

FCC stores operational intelligence. It does not replace CRM systems or project management systems.

No Activities list is provisioned. Relationship activities remain in CRM systems such as RE NXT Actions or Salesforce Tasks. Operational activities remain in planning systems such as Planner, Asana, Smartsheet, or Microsoft Project.

---

# Provisioning Scope

Provision the following SharePoint Lists:

| CSV template | SharePoint List | Purpose |
| --- | --- | --- |
| `programs_template.csv` | Programs | Strategic fundraising areas. |
| `initiatives_template.csv` | Initiatives | Managed operational work portfolios. |
| `commitments_template.csv` | Commitments | Obligations requiring follow-up or completion. |
| `dependencies_template.csv` | Dependencies | Blockers, prerequisites, and cross-functional dependencies. |
| `risks_template.csv` | Risks | Manual or system-generated operational risks. |
| `knowledge_template.csv` | Knowledge | Metadata for operational knowledge assets. |
| `metric_snapshots_template.csv` | Metric Snapshots | Historical calculated management metrics and approved placeholders. |
| `configuration_template.csv` | Configuration | Client-specific settings, thresholds, weights, and escalation rules. |

Provision the following SharePoint Document Libraries:

| Library | Purpose |
| --- | --- |
| Data Drop | Stores imported source-system files. |
| Knowledge Library | Stores SOPs, policies, playbooks, templates, post-mortems, and decision logs. |

---

# Choice Values

Choice values listed in this plan are MVP implementation defaults. They are not canonical model definitions.

The canonical model defines the objects and required attributes. Client-specific choice values, source mappings, thresholds, and scoring rules should be reviewed through the CRM Mapping Workbook and adjusted in provisioning/configuration assets as implementation matures.

---

# Source Field Standard

CSV files use `source_system` and `source_record_id` consistently for source traceability.

Some SharePoint display labels may use the shorter label `Source`. In those cases, the CSV import field remains `source_system`, and import/provisioning logic should map `source_system` to the SharePoint display column.

---

# Relationship Model

The authoritative parent path is:

```text
Programs
  -> Initiatives
      -> Commitments
      -> Dependencies
      -> Risks
      -> Knowledge
      -> Metric Snapshots
```

Provision lookup relationships as follows:

| Source List | Field | Target List | Required | Notes |
| --- | --- | --- | --- | --- |
| Initiatives | Program | Programs | Yes | Every Initiative belongs to one Program. |
| Commitments | Initiative | Initiatives | Yes | No direct Program lookup. Program is inferred through Initiative. |
| Dependencies | Initiative | Initiatives | Yes | No direct Program lookup. |
| Risks | Initiative | Initiatives | Yes | No direct Program lookup. |
| Knowledge | Initiative | Initiatives | No | Optional because some assets are organization-wide. |
| Metric Snapshots | Initiative | Initiatives | No | Optional for organization-wide or future program-level metrics. |

Do not provision direct Program lookups on Commitments, Dependencies, Risks, Knowledge, or Metric Snapshots. Power BI should resolve Program-level reporting through `Initiative -> Program`.

---

# List Column Mapping

## Programs

CSV template: `programs_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `program_id` | Program ID | Single line text | Yes |
| `program_name` | Program Name | Single line text | Yes |
| `program_type` | Program Type | Choice | Yes |
| `executive_owner` | Executive Owner | Person | No |
| `department` | Department | Choice | No |
| `status` | Status | Choice | Yes |
| `strategic_goal` | Strategic Goal | Multiple lines text | No |
| `start_date` | Start Date | Date | No |
| `end_date` | End Date | Date | No |

Suggested MVP choices:

- Program Type: Annual Giving, Major Gifts, Events, Stewardship, Corporate Partnerships, Capital Campaign, Other
- Status: Active, Inactive

Recommended indexes: Program ID, Program Name, Status.

---

## Initiatives

CSV template: `initiatives_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `initiative_id` | Initiative ID | Single line text | Yes |
| `initiative_name` | Initiative Name | Single line text | Yes |
| `program` | Program | Lookup to Programs | Yes |
| `initiative_type` | Initiative Type | Choice | Yes |
| `owner` | Owner | Person | No |
| `department` | Department | Choice | No |
| `status` | Status | Choice | Yes |
| `start_date` | Start Date | Date | No |
| `target_date` | Target Date | Date | No |
| `goal_amount` | Goal Amount | Currency | No |
| `readiness_score` | Readiness Score | Number | No |
| `risk_score` | Risk Score | Number | No |
| `source_system` | Source System | Choice | No |
| `source_record_id` | Source Record ID | Single line text | No |

Suggested MVP choices:

- Initiative Type: Portfolio, Appeal, Event, Program Cycle, Campaign, Other
- Status: Active, Complete, On Hold, At Risk
- Source System: RE NXT, Salesforce, Planner, Asana, Smartsheet, Excel, Manual, Other

Recommended indexes: Initiative ID, Program, Status, Owner, Source System.

---

## Commitments

CSV template: `commitments_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `commitment_id` | Commitment ID | Single line text | Yes |
| `commitment_name` | Commitment Name | Single line text | Yes |
| `initiative` | Initiative | Lookup to Initiatives | Yes |
| `commitment_type` | Commitment Type | Choice | Yes |
| `owner` | Owner | Person | No |
| `due_date` | Due Date | Date | Yes |
| `status` | Status | Choice | Yes |
| `priority` | Priority | Choice | No |
| `value_amount` | Value Amount | Currency | No |
| `source_system` | Source System | Choice | No |
| `source_record_id` | Source Record ID | Single line text | No |
| `escalation_level` | Escalation Level | Choice | No |
| `notes` | Notes | Multiple lines text | No |

Suggested MVP choices:

- Commitment Type: Donor Follow-Up, Proposal, Stewardship, Operational, Executive Briefing, Vendor, Other
- Status: Open, Completed, Overdue
- Priority: Low, Medium, High
- Source System: RE NXT, RE NXT Actions, Salesforce, Planner, Asana, Smartsheet, Excel, Manual, Power Automate, Other
- Escalation Level: None, Manager, Director

Recommended indexes: Commitment ID, Initiative, Due Date, Status, Owner, Priority.

---

## Dependencies

CSV template: `dependencies_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `dependency_id` | Dependency ID | Single line text | Yes |
| `dependency_name` | Dependency Name | Single line text | Yes |
| `initiative` | Initiative | Lookup to Initiatives | Yes |
| `dependency_type` | Dependency Type | Choice | Yes |
| `blocking_area` | Blocking Area | Choice | No |
| `impacted_area` | Impacted Area | Choice | No |
| `owner` | Owner | Person | No |
| `due_date` | Due Date | Date | No |
| `status` | Status | Choice | Yes |
| `severity` | Severity | Choice | Yes |
| `impact_description` | Impact Description | Multiple lines text | No |
| `resolution_notes` | Resolution Notes | Multiple lines text | No |

Suggested MVP choices:

- Dependency Type: Approval, Resource, Technology, Vendor, Review, Finance, Legal, Other
- Blocking Area: Finance, Legal, Marketing, Leadership, Prospect Research, IT, Operations, External Vendor, Other
- Impacted Area: Annual Giving, Major Gifts, Events, Stewardship, Corporate Partnerships, Operations, Other
- Status: Open, Resolved
- Severity: Low, Medium, High

Recommended indexes: Dependency ID, Initiative, Status, Severity, Due Date.

---

## Risks

CSV template: `risks_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `risk_id` | Risk ID | Single line text | Yes |
| `risk_name` | Risk Name | Single line text | Yes |
| `initiative` | Initiative | Lookup to Initiatives | Yes |
| `risk_type` | Risk Type | Choice | Yes |
| `severity` | Severity | Choice | Yes |
| `likelihood` | Likelihood | Choice | Yes |
| `status` | Status | Choice | Yes |
| `owner` | Owner | Person | No |
| `date_identified` | Date Identified | Date | Yes |
| `target_resolution_date` | Target Resolution Date | Date | No |
| `source_system` | Source | Choice | No |
| `source_record_id` | Source Record ID | Single line text | No |
| `mitigation_plan` | Mitigation Plan | Multiple lines text | No |

Suggested MVP choices:

- Risk Type: Pipeline, Operational, Data Quality, Staffing, Readiness, Follow-Up, Commitment, Dependency, Governance, Other
- Severity: Low, Medium, High
- Likelihood: Low, Medium, High
- Status: Open, Monitoring, Resolved
- Source System: RE NXT, RE NXT Actions, Salesforce, Planner, Asana, Smartsheet, Manual, Power Automate, Other

Recommended indexes: Risk ID, Initiative, Severity, Status, Date Identified, Owner.

---

## Knowledge

CSV template: `knowledge_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `knowledge_id` | Knowledge ID | Single line text | Yes |
| `title` | Title | Single line text | Yes |
| `knowledge_type` | Knowledge Type | Choice | Yes |
| `initiative` | Initiative | Lookup to Initiatives | No |
| `owner` | Owner | Person | No |
| `status` | Status | Choice | Yes |
| `source_authority` | Source Authority | Choice | No |
| `review_date` | Review Date | Date | No |
| `document_link` | Document Link | Hyperlink | No |
| `tags` | Tags | Managed metadata or text | No |

Suggested MVP choices:

- Knowledge Type: SOP, Policy, Playbook, Template, Checklist, Lesson Learned, Post-Mortem, Decision Log, Other
- Status: Draft, Approved, Archived
- Source Authority: Working, Approved, Official

Recommended indexes: Knowledge ID, Status, Review Date, Owner, Initiative.

---

## Metric Snapshots

CSV template: `metric_snapshots_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `snapshot_id` | Snapshot ID | Single line text | Yes |
| `snapshot_date` | Snapshot Date | Date | Yes |
| `initiative` | Initiative | Lookup to Initiatives | No |
| `metric_name` | Metric Name | Choice or single line text | Yes |
| `metric_value` | Metric Value | Number | No |
| `metric_unit` | Metric Unit | Choice | No |
| `threshold_status` | Threshold Status | Choice | No |
| `source_system` | Source | Choice | No |
| `notes` | Notes | Multiple lines text | No |

Suggested MVP metric names:

- open_commitments_count
- overdue_commitments_count
- open_dependencies_count
- high_risks_count
- commitment_compliance_placeholder
- follow_up_compliance_placeholder

Readiness score snapshots may be added only when supplied as an approved config input, checklist result, or future rule output. Sprint 1 provisioning should not assume a readiness calculation formula.

Suggested MVP choices:

- Metric Unit: Count, Percent, Score, Currency, Days
- Threshold Status: Healthy, Good, Warning, Critical, Not Evaluated
- Source System: Power Automate, Power BI, Manual, Import, Other

Recommended indexes: Snapshot ID, Snapshot Date, Initiative, Metric Name, Threshold Status.

---

## Configuration

CSV template: `configuration_template.csv`

| CSV column | SharePoint column | Type | Required |
| --- | --- | --- | --- |
| `config_id` | Config ID | Single line text | Yes |
| `config_area` | Config Area | Choice | Yes |
| `config_name` | Config Name | Single line text | Yes |
| `config_value` | Config Value | Single line text | Yes |
| `effective_date` | Effective Date | Date | No |
| `status` | Status | Choice | Yes |
| `notes` | Notes | Multiple lines text | No |

Suggested MVP choices:

- Config Area: Follow-Up SLA, Risk Thresholds, Readiness Weights, Escalation Rules, Snapshot Rules, Source Mapping, Other
- Status: Active, Inactive

Recommended indexes: Config ID, Config Area, Config Name, Status.

---

# Required Field Strategy

At minimum, require:

| List | Required fields |
| --- | --- |
| Programs | Program ID, Program Name, Program Type, Status |
| Initiatives | Initiative ID, Initiative Name, Program, Initiative Type, Status |
| Commitments | Commitment ID, Commitment Name, Initiative, Commitment Type, Due Date, Status |
| Dependencies | Dependency ID, Dependency Name, Initiative, Dependency Type, Status, Severity |
| Risks | Risk ID, Risk Name, Initiative, Risk Type, Severity, Likelihood, Status, Date Identified |
| Knowledge | Knowledge ID, Title, Knowledge Type, Status |
| Metric Snapshots | Snapshot ID, Snapshot Date, Metric Name |
| Configuration | Config ID, Config Area, Config Name, Config Value, Status |

Person fields should not be required in the MVP because imported CSV data may contain display names that require later identity resolution.

---

# CSV Import Considerations

CSV column names use snake_case. SharePoint display names use title case.

During import:

1. Load Programs first.
2. Load Initiatives second and resolve `program` to the Programs lookup.
3. Load Commitments, Dependencies, Risks, Knowledge, and Metric Snapshots after Initiatives exist.
4. Load Configuration independently.
5. Treat source activity extracts as staging data, not as FCC-owned list records.

Lookup resolution should accept stable IDs where possible:

| CSV field | Preferred lookup value |
| --- | --- |
| `program` | `program_id` from Programs |
| `initiative` | `initiative_id` from Initiatives |

If importing manually through SharePoint, lookup display values may need to match list item titles. For automated provisioning, keep the stable FCC IDs and resolve them through script or flow logic.

---

# Future PnP Provisioning Considerations

Future provisioning assets may be implemented with PnP PowerShell or PnP provisioning templates.

Recommended approach:

1. Create the SharePoint site or confirm an existing site.
2. Create document libraries before data ingestion.
3. Create base lists without lookup fields first.
4. Add lookup fields after target lists exist.
5. Add choice columns using MVP defaults, then adjust per approved mapping decisions.
6. Add indexed columns for high-use filters and Power BI refresh stability.
7. Add default views for operational use and data QA.
8. Import seed data only after schema provisioning succeeds.

Potential PnP assets:

| Asset | Purpose |
| --- | --- |
| `sharepoint/pnp/provision-lists.ps1` | Creates lists, columns, lookups, and indexes. |
| `sharepoint/pnp/schema.json` | Machine-readable schema definition for lists and fields. |
| `sharepoint/pnp/import-seed-data.ps1` | Imports CSV data and resolves lookups. |
| `sharepoint/pnp/README.md` | Operational instructions for tenant admins. |

Provisioning should use internal field names that are stable and CSV-compatible where practical, for example `ProgramID`, `InitiativeID`, `SourceSystem`, and `SourceRecordID`. Display names can remain user-friendly.

---

# PnP Field Type Guidance

| SharePoint type | PnP consideration |
| --- | --- |
| Single line text | Use for stable FCC IDs, names, and source record IDs. |
| Multiple lines text | Use plain text unless rich text is explicitly required. |
| Choice | Define MVP defaults in provisioning assets and avoid free-form drift. |
| Person | Allow optional values during MVP imports; resolve display names after ingestion if needed. |
| Date | Use date-only values for CSV imports unless time is required later. |
| Currency | Use tenant/default currency unless client-specific requirements exist. |
| Number | Use for scores, counts, percentages, and metric values. Allow blanks for explicit placeholders. |
| Hyperlink | Use for Knowledge document links. |
| Lookup | Add after target list creation; do not create circular lookup paths. |
| Managed metadata | Defer unless the tenant taxonomy is known; use text tags for MVP if needed. |

---

# Views To Provision

Recommended default views:

| List | View | Filters or sorting |
| --- | --- | --- |
| Programs | Active Programs | Status = Active |
| Initiatives | Active Initiatives | Status = Active, grouped by Program |
| Commitments | Open and Overdue Commitments | Status != Completed, sorted by Due Date |
| Dependencies | Open Dependencies | Status = Open, sorted by Severity and Due Date |
| Risks | Open High Risks | Status != Resolved, Severity = High |
| Knowledge | Review Due | Review Date before or near today, Status != Archived |
| Metric Snapshots | Recent Snapshots | Sorted by Snapshot Date descending |
| Configuration | Active Configuration | Status = Active, grouped by Config Area |

---

# Validation Before Provisioning

Before importing CSV data into SharePoint, run:

```bash
python scripts/validate_fcc_csvs.py
```

To validate generated overlay data, run:

```bash
python scripts/validate_fcc_csvs.py --input-dir data/operational_overlay
```

The validator checks required columns, missing IDs, date formats, status values, and broken Program or Initiative references.

---

# Out Of Scope For MVP

Do not provision:

- Activities list
- CRM write-back lists
- Donor contact or donor notes lists
- Multi-CRM integration framework lists
- Predictive analytics tables
- Dataverse tables

These exclusions preserve the MVP boundary: FCC manages operational intelligence, not source-system execution records.
