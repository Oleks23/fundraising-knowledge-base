# PBIX Build Checklist

# Fundraising Command Centre (FCC)

Version: 1.0

---

# Purpose

This checklist guides a manual Power BI Desktop build for the FCC Microsoft 365 MVP using the Sprint 2 data layer, relationship model, DAX measures, and wireframe specs.

Use this as a build sequence, not as a new architecture definition. The PBIX should follow the existing MVP constraints:

- Do not create an Activities table.
- Do not create Activities pages or Activities visuals.
- Do not use Program-level or Executive-level readiness or risk score rollups.
- Do not use a conformed Owner slicer in MVP.
- Do not invent new DAX measures.
- Use object-specific owner fields only, such as `Initiatives[owner]`, `Commitments[owner]`, `Dependencies[owner]`, `Risks[owner]`, `Knowledge[owner]`, and `Programs[executive_owner]`.

---

# Source Files

Use these repository files during the manual build:

| Area | File or folder |
| --- | --- |
| Power Query scripts | `powerbi/m/*.pq` |
| Power Query notes | `powerbi/m/README.md` |
| Relationships | `powerbi/model/RELATIONSHIPS.md` |
| DAX measures | `powerbi/dax/core_measures.dax` |
| DAX notes | `powerbi/dax/README.md` |
| Page specifications | `docs/POWER_BI_PAGE_SPECS.md` |
| Wireframes | `powerbi/pages/WIREFRAME_SPECS.md` |
| Validation data | `data/sample/*.csv` |

---

# 1. Create A New PBIX File

1. Open Power BI Desktop.
2. Create a new blank report.
3. Save the file as `FCC_MVP.pbix` or another clear local working name.
4. Confirm the file is a manual build artifact and is not replacing any source CSV, M, DAX, or documentation file.
5. Set the report canvas to 16:9.

Do not add report pages for Activities.

---

# 2. Create The `SourceFolder` Parameter

1. Open Power Query Editor.
2. Create a text parameter named `SourceFolder`.
3. Set the parameter value to the local folder containing the sample CSV files.
4. For the Sprint 2 validation build, point it to the local checkout folder ending in `data/sample`.

Example value:

```text
C:\Users\amoro\OneDrive\Documents\FCC\data\sample
```

Use a local path only inside Power BI Desktop. Do not hardcode that absolute path into the M scripts in the repository.

---

# 3. Load Power Query Scripts From `powerbi/m/`

Create one Power Query table per script:

| Query name | Script | CSV loaded | FCC object |
| --- | --- | --- | --- |
| Programs | `Programs.pq` | `programs.csv` | Program |
| Initiatives | `Initiatives.pq` | `initiatives.csv` | Initiative |
| Commitments | `Commitments.pq` | `commitments.csv` | Commitment |
| Dependencies | `Dependencies.pq` | `dependencies.csv` | Dependency |
| Risks | `Risks.pq` | `risks.csv` | Risk |
| Knowledge | `Knowledge.pq` | `knowledge.csv` | Knowledge |
| MetricSnapshots | `MetricSnapshots.pq` | `metric_snapshots.csv` | Metric Snapshot |
| Configuration | `Configuration.pq` | `configuration.csv` | Configuration |

Manual load steps:

1. In Power Query Editor, create a blank query.
2. Open Advanced Editor.
3. Paste the contents of the matching `.pq` script.
4. Name the query exactly as listed above.
5. Repeat for all eight MVP tables.
6. Confirm no Activities query exists.
7. Close and apply after all queries load successfully.

---

# 4. Set And Verify Data Types

The M scripts apply expected data types. After loading, verify them in Power Query and Model view.

## Key Type Checks

| Table | Text fields | Date fields | Numeric fields |
| --- | --- | --- | --- |
| Programs | `program_id`, `program_name`, `status`, `department`, `executive_owner` | `start_date`, `target_date` | `goal_amount` |
| Initiatives | `initiative_id`, `initiative_name`, `program`, `status`, `owner`, `source_system`, `source_record_id` | `start_date`, `target_date` | `goal_amount`, `readiness_score`, `risk_score` |
| Commitments | `commitment_id`, `commitment_name`, `initiative`, `status`, `owner`, `priority`, `source_system`, `source_record_id` | `due_date`, `completed_date` | `value_amount` |
| Dependencies | `dependency_id`, `dependency_name`, `initiative`, `status`, `severity`, `owner` | `due_date`, `resolved_date` | none expected |
| Risks | `risk_id`, `risk_name`, `initiative`, `status`, `severity`, `likelihood`, `owner`, `source_system`, `source_record_id` | `date_identified`, `target_resolution_date`, `resolved_date` | none expected |
| Knowledge | `knowledge_id`, `title`, `initiative`, `status`, `owner`, `source_authority`, `document_link` | `review_date` | none expected |
| MetricSnapshots | `snapshot_id`, `initiative`, `metric_name`, `metric_unit`, `source_system` | `snapshot_date` | `metric_value` |
| Configuration | `config_id`, `config_area`, `config_name`, `config_value`, `status` | `effective_date` | none expected |

Status normalization should follow the M scripts and DAX assumptions. Knowledge status must remain separate from operational status.

---

# 5. Create Relationships

Create relationships manually in Model view using natural IDs for the MVP.

| From table | From column | To table | To column | Cardinality | Filter direction | Active |
| --- | --- | --- | --- | --- | --- | --- |
| Programs | `program_id` | Initiatives | `program` | One-to-many | Single | Yes |
| Initiatives | `initiative_id` | Commitments | `initiative` | One-to-many | Single | Yes |
| Initiatives | `initiative_id` | Dependencies | `initiative` | One-to-many | Single | Yes |
| Initiatives | `initiative_id` | Risks | `initiative` | One-to-many | Single | Yes |
| Initiatives | `initiative_id` | Knowledge | `initiative` | One-to-many | Single | Yes |
| Initiatives | `initiative_id` | MetricSnapshots | `initiative` | One-to-many | Single | Yes |

Relationship rules:

- Program filtering must flow through `Programs -> Initiatives -> child tables`.
- Do not create direct relationships from Programs to Commitments, Dependencies, Risks, Knowledge, or MetricSnapshots.
- Keep relationships single-direction from dimensions to facts.
- Keep Configuration disconnected unless a future approved model change says otherwise.
- Do not create an Activities relationship.

Optional future Date, Owner, Status, Source System, and type dimensions are documented in `powerbi/model/RELATIONSHIPS.md`, but they are not required for this MVP manual build.

---

# 6. Add DAX Measures

Add measures from `powerbi/dax/core_measures.dax` exactly as written.

Recommended organization:

1. Create a display folder named `Commitments` and add:
   - `Open Commitments`
   - `Completed Commitments`
   - `Overdue Commitments`
   - `Commitments Due Next 7 Days`
   - `Commitment Completion Rate`
2. Create a display folder named `Dependencies` and add:
   - `Open Dependencies`
   - `Resolved Dependencies`
   - `Overdue Dependencies`
   - `High Severity Dependencies`
3. Create a display folder named `Risks` and add:
   - `Open Risks`
   - `High Risks`
   - `Critical Risks`
   - `Resolved Risks`
   - `Initiatives At Risk`
4. Create a display folder named `Metric Snapshots` and add:
   - `Latest Snapshot Date`
   - `Open Commitments Latest`
   - `Overdue Commitments Latest`
   - `Open Dependencies Latest`
   - `High Risks Latest`
   - `Follow-Up Compliance Placeholder Latest`
   - `Commitment Compliance Placeholder Latest`
   - `Readiness Score Placeholder Latest`
   - `Risk Score Placeholder Latest`
5. Create a display folder named `Initiatives` and add:
   - `Active Initiatives`
   - `Completed Initiatives`
   - `Average Readiness Score`
   - `Average Risk Score`

Build rules:

- Do not create Activities measures.
- Do not create a generic `Latest Metric Value` measure.
- Do not add new readiness or risk formulas.
- Treat `readiness_score`, `risk_score`, `readiness_score_placeholder`, and `risk_score_placeholder` as imported inputs only.
- Use Initiative-level score placeholder measures only where `Initiatives[initiative_id]` is in filter or drill context.
- Do not use `Average Readiness Score` or `Average Risk Score` for Program or Executive rollup cards.

---

# 7. Build Report Pages In Order

Create the six MVP report pages in this exact order.

## Page 1: Executive Control Tower

Purpose: leadership view of what is at risk, overdue, blocked, or requiring intervention.

Build:

1. Header with page title and `Latest Snapshot Date`.
2. Slicers:
   - `Programs[program_name]`
   - `Programs[department]`
   - `Programs[executive_owner]`
   - `Initiatives[status]`
   - `MetricSnapshots[snapshot_date]`
3. KPI cards:
   - `Active Initiatives`
   - `Open Commitments Latest`
   - `Overdue Commitments Latest`
   - `Open Dependencies Latest`
   - `High Risks Latest`
   - `Critical Risks`
   - `Initiatives At Risk`
   - `Follow-Up Compliance Placeholder Latest`
   - `Commitment Compliance Placeholder Latest`
4. Charts from `powerbi/pages/WIREFRAME_SPECS.md`:
   - Program Operational Load
   - Initiatives Requiring Intervention
   - Risk Severity Mix
   - Commitment Status Mix
   - Count Snapshot Trend filtered to count metrics only
5. Tables:
   - Top Intervention List
   - High/Critical Risks
   - Overdue Commitments

Do not show Executive readiness or risk score cards.

## Page 2: Work Portfolio

Purpose: Program and Initiative inventory with ownership, lifecycle state, target dates, and operational load.

Build:

1. Slicers:
   - `Programs[program_name]`
   - `Initiatives[initiative_id]`, with `Initiatives[initiative_name]` as readable label where practical
   - `Initiatives[status]`
   - `Initiatives[initiative_type]`
   - `Initiatives[owner]`
   - `Initiatives[department]`
   - `Initiatives[target_date]`
2. KPI cards:
   - `Active Initiatives`
   - `Completed Initiatives`
   - `Initiatives At Risk`
   - `Open Commitments`
   - `Open Dependencies`
   - `Open Risks`
3. Charts:
   - Initiative Portfolio Matrix
   - Initiative Status by Program
   - Initiative Owner Workload using `Initiatives[owner]` only
   - Target Date Timeline
4. Tables:
   - Initiative Register
   - Portfolio Risk/Execution Summary

Do not build Future Conformed Owner Workload in the MVP.

## Page 3: Readiness & Execution

Purpose: Initiative-level imported score placeholders and execution pressure.

Build:

1. Slicers:
   - `Programs[program_name]`
   - `Initiatives[initiative_id]`
   - `Initiatives[initiative_name]` as readable label only
   - `Initiatives[owner]`
   - `Initiatives[status]`
   - `MetricSnapshots[snapshot_date]`
   - `MetricSnapshots[threshold_status]`
2. KPI cards:
   - `Readiness Score Placeholder Latest`
   - `Risk Score Placeholder Latest`
   - `Open Commitments Latest`
   - `Overdue Commitments Latest`
   - `Open Dependencies Latest`
   - `High Risks Latest`
   - `Commitments Due Next 7 Days`
3. Charts:
   - Initiative Readiness Snapshot
   - Execution Pressure Trend filtered to count metrics only
   - Commitments by Due Window
   - Dependencies Blocking Execution
   - Risks by Type and Severity
4. Tables:
   - Readiness Metric Snapshots
   - Execution Commitments
   - Blocking Dependencies
   - Readiness Risks

Score placeholder cards must be blank or muted unless `Initiatives[initiative_id]` is in context. Do not calculate readiness from operational counts.

## Page 4: Dependencies & Risks

Purpose: blocker and risk intervention view.

Build:

1. Slicers:
   - `Programs[program_name]`
   - `Initiatives[initiative_id]`, with `Initiatives[initiative_name]` as readable label where practical
   - `Dependencies[dependency_type]`
   - `Dependencies[blocking_area]`
   - `Dependencies[impacted_area]`
   - `Dependencies[status]`
   - `Dependencies[severity]`
   - `Risks[risk_type]`
   - `Risks[severity]`
   - `Risks[status]`
   - `Dependencies[owner]`
   - `Risks[owner]`
   - `Dependencies[due_date]`
   - `Risks[target_resolution_date]`
2. KPI cards:
   - `Open Dependencies`
   - `Overdue Dependencies`
   - `High Severity Dependencies`
   - `Open Risks`
   - `High Risks`
   - `Critical Risks`
   - `Initiatives At Risk`
3. Charts:
   - Dependency Blocker Map
   - Risk Severity by Program
   - Risk Type Mix
   - Dependency Due Timeline
   - Risk Resolution Timeline
4. Tables:
   - Dependency Register
   - Risk Register
   - At-Risk Initiatives

Use `Dependencies[owner]` and `Risks[owner]` separately. Do not create a cross-object owner slicer.

## Page 5: Commitments & Follow-Up

Purpose: accountability, overdue work, due-soon commitments, and compliance placeholders.

Build:

1. Slicers:
   - `Programs[program_name]`
   - `Initiatives[initiative_id]`, with `Initiatives[initiative_name]` as readable label where practical
   - `Commitments[owner]`
   - `Commitments[commitment_type]`
   - `Commitments[status]`
   - `Commitments[priority]`
   - `Commitments[escalation_level]`
   - `Commitments[due_date]`
   - `Commitments[source_system]`
2. KPI cards:
   - `Open Commitments`
   - `Completed Commitments`
   - `Overdue Commitments`
   - `Commitments Due Next 7 Days`
   - `Commitment Completion Rate`
   - `Follow-Up Compliance Placeholder Latest`
   - `Commitment Compliance Placeholder Latest`
3. Charts:
   - Commitments by Status
   - Overdue by Commitment Owner
   - Due Date Calendar or Timeline
   - Commitment Type Mix
   - Compliance Placeholder Trend filtered to `follow_up_compliance` and `commitment_compliance`
4. Tables:
   - Commitment Work Queue
   - Overdue Commitments
   - Source Traceability

Do not show RE NXT Actions, Planner tasks, or any other source Activities as FCC-owned rows.

## Page 6: Knowledgebase

Purpose: knowledge asset coverage, stewardship, status, and review needs.

Build:

1. Slicers:
   - `Programs[program_name]`
   - `Initiatives[initiative_id]`, with `Initiatives[initiative_name]` as readable label where practical
   - `Knowledge[knowledge_type]`
   - `Knowledge[status]`
   - `Knowledge[source_authority]`
   - `Knowledge[owner]`
   - `Knowledge[review_date]`
   - `Knowledge[tags]`
2. KPI cards using implicit counts or visual-level filters:
   - Count of `Knowledge[knowledge_id]`
   - Count of `Knowledge[knowledge_id]` filtered to `Knowledge[status] = "Approved"`
   - Count of `Knowledge[knowledge_id]` filtered to `Knowledge[status] = "Draft"`
   - Visual-level count of overdue review assets, if needed
   - Visual-level count of blank `Knowledge[owner]`, if needed
3. Charts:
   - Knowledge by Program and Initiative
   - Knowledge Status Mix
   - Review Calendar
   - Source Authority Mix
   - Tag Explorer
4. Tables:
   - Knowledge Asset Register
   - Assets Due For Review
   - Initiative Knowledge Coverage

Do not reuse operational status measures for Knowledge. Knowledge status is separate from Commitment, Dependency, and Risk status.

---

# 8. Add Slicers And Conditional Formatting

## Slicer Rules

- Use Program slicers from `Programs[program_name]`.
- Use Initiative ID where score placeholders or drill context matters: `Initiatives[initiative_id]`.
- Display `Initiatives[initiative_name]` as the readable label where Power BI visual setup allows.
- Use object-specific owners only:
  - `Programs[executive_owner]`
  - `Initiatives[owner]`
  - `Commitments[owner]`
  - `Dependencies[owner]`
  - `Risks[owner]`
  - `Knowledge[owner]`
- Do not create one Owner slicer that filters all objects.

## Conditional Formatting Rules

Use simple MVP-safe rules:

| Signal | MVP rule |
| --- | --- |
| Open count card | Red if count > 0; green if count = 0. |
| Overdue count card | Red if count > 0; green if count = 0. |
| High or Critical risk count | Red if count > 0; green if count = 0. |
| High severity dependency count | Red if count > 0; green if count = 0. |
| Due within 7 days | Yellow if count > 0; green if count = 0. |
| Past due date or past target date | Red. |
| Placeholder compliance blank | Muted or neutral with placeholder label. |
| Score placeholder blank | Muted or neutral. |

Threshold-based formatting is future/config-driven and should not be implemented in the MVP unless configuration-backed thresholds are added.

Do not use color to imply calculated readiness or calculated risk scoring.

---

# 9. Validate KPIs Against `data/sample/`

After loading data and creating relationships/measures, validate the report against the sample CSV files.

## Data Load Validation

1. Confirm all eight MVP tables load:
   - Programs
   - Initiatives
   - Commitments
   - Dependencies
   - Risks
   - Knowledge
   - MetricSnapshots
   - Configuration
2. Confirm no Activities table is present.
3. Confirm `source_system` and `source_record_id` are preserved where present.
4. Confirm row counts match the corresponding CSV files in `data/sample/`.

## Relationship Validation

1. Select a Program and confirm related Initiatives filter correctly.
2. Select an Initiative and confirm Commitments, Dependencies, Risks, Knowledge, and MetricSnapshots filter correctly.
3. Confirm child facts are not directly related to Programs.
4. Confirm Configuration remains disconnected.

## KPI Validation

Validate each KPI against a filtered table visual showing the underlying rows.

| KPI | Validation approach |
| --- | --- |
| `Open Commitments` | Count Commitments whose status is not completed/closed. |
| `Completed Commitments` | Count Commitments with completed status. |
| `Overdue Commitments` | Count non-completed Commitments with `Commitments[due_date] < TODAY()`. |
| `Commitments Due Next 7 Days` | Count non-completed Commitments due from today through seven days out. |
| `Commitment Completion Rate` | Compare completed commitments divided by all commitments in context. |
| `Open Dependencies` | Count unresolved/open Dependencies. |
| `Resolved Dependencies` | Count resolved Dependencies. |
| `Overdue Dependencies` | Count unresolved Dependencies with `Dependencies[due_date] < TODAY()`. |
| `High Severity Dependencies` | Count unresolved high-severity Dependencies. |
| `Open Risks` | Count unresolved Risks. |
| `High Risks` | Count unresolved high-severity Risks. |
| `Critical Risks` | Count unresolved critical Risks. |
| `Initiatives At Risk` | Count distinct Initiatives with unresolved High or Critical risks. |
| Latest snapshot count measures | Compare to `MetricSnapshots` rows at the latest `snapshot_date` in the current filter context. |
| Compliance placeholder measures | Confirm they average imported placeholder values only. |
| Score placeholder measures | Confirm they show only at Initiative context using `Initiatives[initiative_id]`. |

## Page Validation

1. Executive Control Tower answers what is at risk, overdue, blocked, or requiring intervention.
2. Work Portfolio shows Program and Initiative inventory without cross-object owner slicing.
3. Readiness & Execution shows Initiative-level imported score placeholders only.
4. Dependencies & Risks shows blockers and risks through Initiative relationships.
5. Commitments & Follow-Up shows FCC-owned commitments and source lineage only.
6. Knowledgebase keeps Knowledge status separate from operational status.

---

# 10. Known MVP Limitations

- CSV files are the MVP source. Live SharePoint, CRM, Planner, or API connectors are not part of this PBIX build.
- Activities remain outside the core model. RE NXT Actions, Planner tasks, and other source activities are not FCC-owned records.
- No conformed `Dim Owner` exists yet. Owner slicers are object-specific.
- No Date table is created by the current Power Query layer. Date bucketing may use base table date fields or visual-level grouping until a Date table is added later.
- No conformed Status dimension exists yet. Knowledge status remains separate from operational statuses.
- Readiness and risk score placeholders are imported values only. No formula is implemented.
- Program-level and Executive-level readiness/risk score cards must remain absent unless approved higher-level MetricSnapshots are supplied later.
- Compliance metrics are placeholders/simple averages until numerator and denominator fields exist.
- Knowledge-specific explicit DAX measures are not yet part of `core_measures.dax`; use implicit counts or clearly labeled future measures only where documented.
- Configuration is loaded but remains disconnected in the MVP model.

---

# Final Build Gate

Before treating the PBIX as ready for review, confirm:

- All eight MVP tables load from `data/sample/`.
- No Activities table, page, visual, or measure exists.
- Relationships match `powerbi/model/RELATIONSHIPS.md`.
- DAX measures match `powerbi/dax/core_measures.dax` with no invented measures.
- Report pages match `powerbi/pages/WIREFRAME_SPECS.md`.
- Initiative-level score placeholders require `Initiatives[initiative_id]` context.
- Owner visuals and slicers are object-specific.
- Conditional formatting uses MVP-safe rules.
- KPIs reconcile to the sample CSV rows.
