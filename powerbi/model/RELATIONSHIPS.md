# Power BI Model Relationships

# Fundraising Command Centre (FCC)

Version: 1.0

---

# Purpose

This document describes the recommended Power BI relationship model for the FCC Microsoft 365 MVP.

It is based on:

- `docs/CANONICAL_DATA_MODEL.md`
- `docs/SHAREPOINT_LISTS_DESIGN.md`
- `docs/POWER_BI_SEMANTIC_MODEL.md`
- `powerbi/m/*.pq`

No DAX measures are defined in this document.

---

# Recommended Model Shape

Use a star schema where possible, with one intentional snowflake edge:

```text
Dim Program
    -> Dim Initiative
        -> Fact Commitments
        -> Fact Dependencies
        -> Fact Risks
        -> Fact Metric Snapshots
        -> Knowledge
```

Program filters flow to Initiative, then from Initiative to the child facts. Do not create direct Program relationships to Commitments, Dependencies, Risks, Knowledge, or Metric Snapshots.

---

# Source Tables

The Sprint 2 Power Query layer creates the following base tables from `data/sample/*.csv`.

| Query/Table | FCC object | Recommended model role | Source CSV |
| --- | --- | --- | --- |
| Programs | Program | Dimension source | `programs.csv` |
| Initiatives | Initiative | Dimension source | `initiatives.csv` |
| Commitments | Commitment | Fact | `commitments.csv` |
| Dependencies | Dependency | Fact | `dependencies.csv` |
| Risks | Risk | Fact | `risks.csv` |
| Knowledge | Knowledge | Dimension/fact-like metadata table | `knowledge.csv` |
| MetricSnapshots | Metric Snapshot | Fact | `metric_snapshots.csv` |
| Configuration | Configuration | Disconnected configuration/reference table | `configuration.csv` |

---

# Primary Keys

Natural IDs are loaded from the FCC CSV files. Power BI may later introduce surrogate keys in Power Query for relationship integrity, but IDs and keys should remain conceptually distinct.

| Table | Natural primary key | Notes |
| --- | --- | --- |
| Programs | `program_id` | Unique Program identifier. |
| Initiatives | `initiative_id` | Unique Initiative identifier. |
| Commitments | `commitment_id` | Unique Commitment identifier. |
| Dependencies | `dependency_id` | Unique Dependency identifier. |
| Risks | `risk_id` | Unique Risk identifier. |
| Knowledge | `knowledge_id` | Unique Knowledge metadata identifier. |
| MetricSnapshots | `snapshot_id` | Unique Metric Snapshot identifier. |
| Configuration | `config_id` | Unique Configuration row identifier. |

Recommended future surrogate keys:

| Dimension | Suggested surrogate key |
| --- | --- |
| Dim Program | `program_key` |
| Dim Initiative | `initiative_key` |
| Dim Owner | `owner_key` |
| Dim Date | `date_key` or native Date |
| Dim Status | `status_key` |
| Dim Commitment Type | `commitment_type_key` |
| Dim Risk Type | `risk_type_key` |
| Dim Dependency Type | `dependency_type_key` |

---

# Foreign Keys

| Table | Foreign key | References | Required |
| --- | --- | --- | --- |
| Initiatives | `program` | Programs.`program_id` | Yes |
| Commitments | `initiative` | Initiatives.`initiative_id` | Yes |
| Dependencies | `initiative` | Initiatives.`initiative_id` | Yes |
| Risks | `initiative` | Initiatives.`initiative_id` | Yes |
| Knowledge | `initiative` | Initiatives.`initiative_id` | No |
| MetricSnapshots | `initiative` | Initiatives.`initiative_id` | No |

Knowledge and MetricSnapshots may contain blank Initiative references for organization-wide records. In those cases, they should not be forced into an artificial Initiative.

---

# Core Relationships

| From table | From column | To table | To column | Cardinality | Filter direction | Active | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Programs | `program_id` | Initiatives | `program` | One-to-many | Single | Yes | Snowflake edge from Program to Initiative. |
| Initiatives | `initiative_id` | Commitments | `initiative` | One-to-many | Single | Yes | Core accountability fact. |
| Initiatives | `initiative_id` | Dependencies | `initiative` | One-to-many | Single | Yes | Core blocker fact. |
| Initiatives | `initiative_id` | Risks | `initiative` | One-to-many | Single | Yes | Core risk fact. |
| Initiatives | `initiative_id` | Knowledge | `initiative` | One-to-many | Single | Yes | Optional Initiative link; blanks are allowed. |
| Initiatives | `initiative_id` | MetricSnapshots | `initiative` | One-to-many | Single | Yes | Optional Initiative link; blanks are allowed. |

All filters should flow from dimensions to facts. Avoid bidirectional filters unless a specific report requirement proves they are necessary.

---

# Date Relationships

Use a dedicated Date table in the semantic model. The Date table is not created in this Sprint 2 documentation, but it is expected by the semantic model.

| Date table | Fact table | Fact date column | Cardinality | Filter direction | Active | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Dim Date | Commitments | `due_date` | One-to-many | Single | Yes | Primary commitment business date. |
| Dim Date | Dependencies | `due_date` | One-to-many | Single | Yes | Primary dependency due date. |
| Dim Date | Risks | `date_identified` | One-to-many | Single | Yes | Primary risk business date. |
| Dim Date | MetricSnapshots | `snapshot_date` | One-to-many | Single | Yes | Primary snapshot date. |
| Dim Date | Knowledge | `review_date` | One-to-many | Single | Optional | Useful for knowledge review reporting. |
| Dim Date | Configuration | `effective_date` | One-to-many | Single | Optional | Useful for configuration audit reporting. |

If later measures require secondary dates, use inactive relationships and activate them in DAX. Do not create multiple Date dimensions for the MVP unless a clear reporting need emerges.

---

# Recommended Dimensions

The following dimensions should be derived from the base tables in future Power Query work.

| Dimension | Source | Key source field(s) | Notes |
| --- | --- | --- | --- |
| Dim Program | Programs | `program_id` | Required dimension. |
| Dim Initiative | Initiatives | `initiative_id`, `program` | Required dimension; carries Program relationship. |
| Dim Owner | Commitments, Dependencies, Risks, Knowledge, Initiatives | `owner`, `executive_owner` | Conformed owner/person dimension. |
| Dim Department | Programs, Initiatives, owner metadata if available | `department` | Supports department slicing. |
| Dim Date | Calendar table | Date values | Mark as Date table. |
| Dim Status | Commitments, Dependencies, Risks | `status` | Operational status only. |
| Dim Knowledge Status | Knowledge | `status` | Separate from operational status. |
| Dim Commitment Type | Commitments | `commitment_type` | Derived from distinct values, not a SharePoint list. |
| Dim Dependency Type | Dependencies | `dependency_type` | Derived from distinct values, not a SharePoint list. |
| Dim Risk Type | Risks | `risk_type` | Derived from distinct values, not a SharePoint list. |
| Dim Metric | MetricSnapshots | `metric_name`, `metric_unit` | Useful for snapshot slicing. |
| Dim Source System | Tables with `source_system` | `source_system` | Useful for traceability and data quality. |

---

# Fact Tables

| Fact table | Grain | Key fields | Typical measures later |
| --- | --- | --- | --- |
| Commitments | One row per FCC Commitment | `commitment_id`, `initiative`, `due_date`, `status` | Open commitments, overdue commitments, aging, completion rate. |
| Dependencies | One row per FCC Dependency | `dependency_id`, `initiative`, `due_date`, `status`, `severity` | Open dependencies, high severity dependencies, overdue dependencies. |
| Risks | One row per FCC Risk | `risk_id`, `initiative`, `date_identified`, `severity`, `status` | Open risks, high risks, risk trend, resolution rate. |
| MetricSnapshots | One row per metric snapshot | `snapshot_id`, `initiative`, `snapshot_date`, `metric_name` | Current value, trend, variance, change since prior snapshot. |

Knowledge can be modeled as a separate metadata table rather than a standard numeric fact table. It supports knowledgebase reporting such as assets due for review, assets by initiative, and assets missing owners.

Configuration should normally remain disconnected. It stores thresholds and settings, not transactional activity.

---

# Status Modeling

Operational statuses should be conformed across Commitments, Dependencies, and Risks.

| Status value | Applies to |
| --- | --- |
| Open | Commitments, Dependencies, Risks |
| Completed | Commitments |
| Overdue | Commitments, usually derived or rules-generated |
| Resolved | Dependencies, Risks |
| Monitoring | Risks |

Knowledge status should remain separate:

| Status value | Applies to |
| --- | --- |
| Draft | Knowledge |
| Approved | Knowledge |
| Archived | Knowledge |

Do not combine Knowledge status into the operational Dim Status table.

---

# Source System Fields

Keep the following fields in fact and source-traceable tables:

- `source_system`
- `source_record_id`

These fields support lineage, data quality checks, and drill-through to source-system context. They should not be used as relationship keys in the core semantic model unless a future source-system staging model is introduced.

---

# Why Activities Are Excluded

Activities are excluded from the core model because FCC does not own activities.

Relationship activities remain in CRM systems such as RE NXT Actions or Salesforce Tasks. Operational activities remain in tools such as Planner, Asana, Smartsheet, or Microsoft Project.

FCC consumes activity data to derive operational intelligence:

- Commitments
- Risks
- Dependencies
- readiness inputs
- compliance metrics
- metric snapshots

Creating a universal Activities table would duplicate CRM actions and planning-tool tasks. It would also make FCC a parallel task-management system, which conflicts with the canonical architecture.

If activity extracts are needed later, model them as staging tables outside the core star schema. They may feed transformation logic, but they should not become first-class FCC facts in the MVP.

---

# MVP Limitations

- This relationship model documents structure only; it does not create DAX measures.
- Surrogate keys are recommended but not yet generated in Sprint 2 base M queries.
- Date, owner, status, source-system, and type dimensions are documented as next-step model artifacts.
- Readiness and compliance formulas are intentionally deferred until approved rules are defined.
- Organization-wide MetricSnapshots and Knowledge assets may have blank Initiative references and require careful handling in visuals.
