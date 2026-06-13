# Power BI Page Specs

# Fundraising Command Centre (FCC)

Version: 1.0

---

# Purpose

This document defines MVP Power BI report page specifications for the Fundraising Command Centre.

The pages are designed around management questions:

- What is at risk?
- What is overdue?
- What is blocked?
- What requires intervention?
- Where should leadership focus today?

The report uses FCC-owned operational objects and Metric Snapshots. It does not model source-system Activities as FCC-owned records.

---

# Model Assumptions

The report follows the MVP relationship path:

```text
Programs
  -> Initiatives
      -> Commitments
      -> Dependencies
      -> Risks
      -> Knowledge
      -> MetricSnapshots
```

Filters should flow from `Programs[program_id]` to `Initiatives[program]`, then from `Initiatives[initiative_id]` to child fact tables. Do not create direct Program-to-fact relationships for report convenience.

Metric Snapshot behavior must follow `docs/METRIC_SNAPSHOT_ROLLUP_RULES.md`:

- Count metrics sum across visible Initiatives at the latest snapshot date.
- Compliance metrics use simple average only as an MVP placeholder.
- Readiness and risk score placeholders are Initiative-level only.
- Program-level and Executive-level readiness/risk scores must remain blank unless explicitly supplied as approved higher-level MetricSnapshots.
- Do not use a generic `Latest Metric Value` measure.

---

# Owner Filtering Limitation

The MVP model does not yet include a conformed `Dim Owner` table.

Owner-based slicers and visuals must be object-specific unless a future owner dimension is built. Use fields such as:

- `Initiatives[owner]`
- `Commitments[owner]`
- `Dependencies[owner]`
- `Risks[owner]`
- `Knowledge[owner]`
- `Programs[executive_owner]`

Do not imply that one Owner slicer filters all FCC objects in the MVP. Any cross-object owner workload visual must be labeled as future-after-Dim-Owner.

---

# Shared Report Filters

Use these common slicers where useful across pages:

| Slicer | Source field | MVP behavior |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter through Initiative relationship path. |
| Initiative | `Initiatives[initiative_name]` | Shared Initiative filter. |
| Initiative Status | `Initiatives[status]` | Initiative lifecycle only. |
| Department | `Programs[department]`, `Initiatives[department]` | Use object-specific field unless a future department dimension is created. |
| Snapshot Date | `MetricSnapshots[snapshot_date]` | Snapshot-specific date filter. |
| Commitment Type | `Commitments[commitment_type]` | Commitment page/filter context. |
| Risk Type | `Risks[risk_type]` | Risk page/filter context. |
| Dependency Type | `Dependencies[dependency_type]` | Dependency page/filter context. |
| Source System | `Commitments[source_system]`, `Risks[source_system]`, `MetricSnapshots[source_system]` | Object-specific lineage filter; not a relationship key. |
| Owner | Object-specific owner fields | No conformed Owner slicer in MVP. |

Use a dedicated Date table when added to the semantic model. Until then, date slicers may use base table date fields for MVP validation.

---

# Shared Drillthrough Pages

The MVP report should support these drillthrough targets:

| Drillthrough target | Context fields | Purpose |
| --- | --- | --- |
| Initiative Detail | `Initiatives[initiative_id]`, `Initiatives[initiative_name]` | Show one Initiative with its commitments, dependencies, risks, knowledge, and latest Initiative-level score placeholders. |
| Program Detail | `Programs[program_id]`, `Programs[program_name]` | Show all Initiatives and aggregated operational facts for one Program. Do not show Program readiness/risk score unless explicitly supplied. |
| Commitment Detail | `Commitments[commitment_id]` | Show `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[source_system]`, `Commitments[source_record_id]`, escalation, and notes. |
| Risk Detail | `Risks[risk_id]` | Show `Risks[severity]`, `Risks[likelihood]`, `Risks[owner]`, `Risks[mitigation_plan]`, `Risks[source_system]`, and `Risks[source_record_id]`. |
| Dependency Detail | `Dependencies[dependency_id]` | Show blocker details, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[severity]`, and resolution notes. |
| Knowledge Detail | `Knowledge[knowledge_id]` | Show knowledge asset metadata, `Knowledge[review_date]`, `Knowledge[owner]`, `Knowledge[status]`, document link, and tags. |

Source-system drillthrough should use `source_system` and `source_record_id` as lineage fields only. Do not imply FCC owns the underlying source activity, task, opportunity, or CRM action.

---

# Page 1: Executive Control Tower

## Purpose

Provide a five-minute leadership view of operational health across all Programs and Initiatives.

This page answers:

- What requires intervention now?
- Which Programs have the most open commitments, blockers, and high risks?
- Where are execution discipline or follow-up indicators weak?

## Primary Users

- CEO / Executive Director
- VP Development
- Campaign leadership
- Directors of fundraising teams
- Operations leadership

## Filters/Slicers

- `Programs[program_name]`
- `Programs[department]`
- `Programs[executive_owner]`
- `Initiatives[status]`
- `MetricSnapshots[snapshot_date]`
- Object-specific `source_system` fields when lineage filtering is needed

Avoid defaulting this page to a single Initiative. It is primarily an Executive and Program-level page.

## KPI Cards

| Card | Measure | Notes |
| --- | --- | --- |
| Active Initiatives | `Active Initiatives` | Count of active Initiative records. |
| Open Commitments | `Open Commitments Latest` | Latest snapshot count; sums across visible Initiatives. |
| Overdue Commitments | `Overdue Commitments Latest` | Latest snapshot count; sums across visible Initiatives. |
| Open Dependencies | `Open Dependencies Latest` | Latest snapshot count; sums across visible Initiatives. |
| High Risks | `High Risks Latest` | Latest snapshot count; sums across visible Initiatives. |
| Critical Risks | `Critical Risks` | Current Risk table count. |
| Initiatives At Risk | `Initiatives At Risk` | Distinct Initiatives with unresolved High/Critical risks. |
| Follow-Up Compliance Placeholder | `Follow-Up Compliance Placeholder Latest` | Label clearly as placeholder/config-input. |
| Commitment Compliance Placeholder | `Commitment Compliance Placeholder Latest` | Label clearly as placeholder/config-input. |

Do not display Program-level or Executive-level readiness score unless an approved higher-level score snapshot is supplied later.

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Program Operational Load | Clustered bar | Axis: `Programs[program_name]`; Values: `Open Commitments Latest`, `Overdue Commitments Latest`, `Open Dependencies Latest`, `High Risks Latest` | Compare operational burden by Program. |
| Initiatives Requiring Intervention | Ranked bar or table | `Initiatives[initiative_name]`, `Overdue Commitments`, `High Risks`, `High Severity Dependencies` | Identify highest-pressure Initiatives. |
| Risk Severity Mix | Stacked bar or donut | `Risks[severity]`, count of `Risks[risk_id]` filtered to open/monitoring status | Show severity composition. |
| Commitment Status Mix | Stacked bar | `Commitments[status]`, count of `Commitments[commitment_id]` | Show current accountability status. |
| Snapshot Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend: `MetricSnapshots[metric_name]`; Values: `MetricSnapshots[metric_value]`; filter to count metrics only | Show recent movement for operational counts. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Top Intervention List | `Programs[program_name]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`, `Overdue Commitments`, `High Risks`, `High Severity Dependencies` |
| High/Critical Risks | `Risks[risk_name]`, `Initiatives[initiative_name]`, `Risks[owner]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[target_resolution_date]`, `Risks[source_system]`, `Risks[source_record_id]` |
| Overdue Commitments | `Commitments[commitment_name]`, `Initiatives[initiative_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |

## Measures Used

- `Active Initiatives`
- `Open Commitments Latest`
- `Overdue Commitments Latest`
- `Open Dependencies Latest`
- `High Risks Latest`
- `Critical Risks`
- `Initiatives At Risk`
- `Follow-Up Compliance Placeholder Latest`
- `Commitment Compliance Placeholder Latest`
- `Overdue Commitments`
- `High Risks`
- `High Severity Dependencies`

## Drillthrough Behavior

- `Programs[program_name]` bar -> Program Detail.
- `Initiatives[initiative_name]` row -> Initiative Detail.
- `Risks[risk_id]` row -> Risk Detail.
- `Commitments[commitment_id]` row -> Commitment Detail.

## Warnings/Limitations

- Compliance cards are MVP placeholders until numerator/denominator fields exist.
- Executive readiness score must not be displayed unless an approved Executive-level MetricSnapshot exists.
- Snapshot cards reflect latest snapshot data, while current-state tables reflect current fact records; label visuals accordingly.
- Do not add source-system task or activity visuals.
- Owner filtering is object-specific in MVP; `Programs[executive_owner]` does not filter all child object owner fields as a conformed person dimension.

## AI Summary Input Fields

Use these fields for Executive summaries:

- Programs: `Programs[program_name]`, `Programs[executive_owner]`, `Programs[department]`, `Programs[status]`
- Initiatives: `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`
- MetricSnapshots: `MetricSnapshots[snapshot_date]`, `MetricSnapshots[metric_name]`, `MetricSnapshots[metric_value]`, `MetricSnapshots[threshold_status]`
- Risks: `Risks[risk_name]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[status]`, `Risks[mitigation_plan]`, `Risks[target_resolution_date]`
- Dependencies: `Dependencies[dependency_name]`, `Dependencies[severity]`, `Dependencies[status]`, `Dependencies[impact_description]`, `Dependencies[due_date]`
- Commitments: `Commitments[commitment_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[escalation_level]`

AI should explain existing measures and records. It should not calculate new KPIs from raw records.

---

# Page 2: Work Portfolio

## Purpose

Show the managed portfolio of Programs and Initiatives, with ownership, status, due dates, and operational load.

This page answers:

- What work portfolios are active?
- Who owns them?
- Which Initiatives need attention?
- How is work distributed across Programs and departments?

## Primary Users

- VP Development
- Directors
- Program owners
- Operations managers
- Portfolio managers

## Filters/Slicers

- `Programs[program_name]`
- `Initiatives[status]`
- `Initiatives[initiative_type]`
- `Initiatives[owner]` as an Initiative-specific owner slicer
- `Initiatives[department]`
- `Initiatives[target_date]`

## KPI Cards

| Card | Measure | Notes |
| --- | --- | --- |
| Active Initiatives | `Active Initiatives` | Primary portfolio count. |
| Completed Initiatives | `Completed Initiatives` | Shows completed Initiative count. |
| Initiatives At Risk | `Initiatives At Risk` | Distinct Initiatives with unresolved High/Critical risks. |
| Open Commitments | `Open Commitments` | Current fact count. |
| Open Dependencies | `Open Dependencies` | Current fact count. |
| Open Risks | `Open Risks` | Current fact count. |

Do not show average Program readiness score. Initiative-level score placeholders may appear only in Initiative-grain tables.

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Initiative Portfolio Matrix | Matrix | Rows: `Programs[program_name]`, `Initiatives[initiative_name]`; Values: `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`, `Open Commitments`, `Open Dependencies`, `High Risks` | Main work inventory. |
| Initiative Status by Program | Stacked bar | Axis: `Programs[program_name]`; Legend: `Initiatives[status]`; Values: count of `Initiatives[initiative_id]` | Show distribution of active/completed/on-hold work. |
| Initiative Owner Workload | Bar chart | Axis: `Initiatives[owner]`; Values: `Active Initiatives` | MVP object-specific owner view for Initiative ownership only. |
| Future Conformed Owner Workload | Bar chart | Axis: future `Dim Owner`; Values: Active Initiatives, Open Commitments, Open Dependencies, Open Risks | Future-after-Dim-Owner only; do not build as MVP cross-object slicer. |
| Target Date Timeline | Timeline or bar by month | Axis: `Initiatives[target_date]` month; Values: count of `Initiatives[initiative_id]` | Show upcoming portfolio milestones. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Initiative Register | `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Programs[program_name]`, `Initiatives[initiative_type]`, `Initiatives[owner]`, `Initiatives[department]`, `Initiatives[status]`, `Initiatives[start_date]`, `Initiatives[target_date]`, `Initiatives[goal_amount]`, `Initiatives[source_system]`, `Initiatives[source_record_id]` |
| Portfolio Risk/Execution Summary | `Initiatives[initiative_name]`, `Initiatives[owner]`, `Open Commitments`, `Overdue Commitments`, `Open Dependencies`, `High Risks`, `Critical Risks` |

## Measures Used

- `Active Initiatives`
- `Completed Initiatives`
- `Initiatives At Risk`
- `Open Commitments`
- `Overdue Commitments`
- `Open Dependencies`
- `Open Risks`
- `High Risks`
- `Critical Risks`
- `High Severity Dependencies`

## Drillthrough Behavior

- `Programs[program_name]` row -> Program Detail.
- `Initiatives[initiative_name]` row -> Initiative Detail.
- `Initiatives[owner]` selection filters Initiative-owned visuals only in MVP.

## Warnings/Limitations

- MVP owner fields are text fields on each object, not a resolved identity dimension.
- One Owner slicer must not be used to filter all objects until a conformed `Dim Owner` exists.
- Program-level scores are intentionally absent.
- Source system fields indicate lineage, not ownership by FCC.

## AI Summary Input Fields

- `Programs[program_name]`, `Programs[program_id]`
- `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[department]`, `Initiatives[target_date]`
- Open/overdue counts from Commitments, Dependencies, and Risks
- `source_system` and `source_record_id` fields for lineage context

---

# Page 3: Readiness & Execution

## Purpose

Show Initiative-level readiness inputs and execution indicators without inventing readiness scoring logic.

This page answers:

- Which Initiatives have execution problems that may affect readiness?
- Which commitments, dependencies, and risks are pressuring readiness?
- What imported Initiative-level readiness/risk placeholders are available?

## Primary Users

- Initiative owners
- Program managers
- Operations leadership
- Readiness reviewers

## Filters/Slicers

- `Programs[program_name]`
- `Initiatives[initiative_name]`
- `Initiatives[owner]` as an Initiative-specific owner slicer
- `Initiatives[status]`
- `MetricSnapshots[snapshot_date]`
- `MetricSnapshots[threshold_status]`

This page should usually require Initiative selection before showing readiness/risk score placeholder cards.

## KPI Cards

| Card | Measure | Notes |
| --- | --- | --- |
| Readiness Score Placeholder | `Readiness Score Placeholder Latest` | Initiative-level only. Blank at Program/Executive level. |
| Risk Score Placeholder | `Risk Score Placeholder Latest` | Initiative-level only. Blank at Program/Executive level. |
| Open Commitments | `Open Commitments Latest` | Latest snapshot count. |
| Overdue Commitments | `Overdue Commitments Latest` | Latest snapshot count. |
| Open Dependencies | `Open Dependencies Latest` | Latest snapshot count. |
| High Risks | `High Risks Latest` | Latest snapshot count. |
| Commitments Due Next 7 Days | `Commitments Due Next 7 Days` | Current fact measure. |

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Initiative Readiness Snapshot | Card group or KPI strip | `Readiness Score Placeholder Latest`, `Risk Score Placeholder Latest`, `Open Commitments Latest`, `Overdue Commitments Latest`, `Open Dependencies Latest`, `High Risks Latest` | Show Initiative-level imported score context. |
| Execution Pressure Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend: `MetricSnapshots[metric_name]`; Value: `MetricSnapshots[metric_value]`; filter to count metrics | Track counts over time for selected Initiative. |
| Commitments by Due Window | Bar chart | Buckets derived from `Commitments[due_date]`; Values: count of `Commitments[commitment_id]` | Show near-term execution pressure. |
| Dependencies Blocking Execution | Bar/table | `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[severity]`, `Dependencies[due_date]` | Identify blockers. |
| Risks by Type and Severity | Stacked bar | `Risks[risk_type]`, `Risks[severity]`, count of `Risks[risk_id]` | Show risk drivers. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Readiness Metric Snapshots | `MetricSnapshots[snapshot_date]`, `Initiatives[initiative_name]`, `MetricSnapshots[metric_name]`, `MetricSnapshots[metric_value]`, `MetricSnapshots[metric_unit]`, `MetricSnapshots[threshold_status]`, `MetricSnapshots[source_system]`, `MetricSnapshots[notes]` |
| Execution Commitments | `Commitments[commitment_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |
| Blocking Dependencies | `Dependencies[dependency_name]`, `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[status]`, `Dependencies[severity]`, `Dependencies[impact_description]` |
| Readiness Risks | `Risks[risk_name]`, `Risks[risk_type]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[owner]`, `Risks[status]`, `Risks[mitigation_plan]`, `Risks[target_resolution_date]` |

## Measures Used

- `Readiness Score Placeholder Latest`
- `Risk Score Placeholder Latest`
- `Open Commitments Latest`
- `Overdue Commitments Latest`
- `Open Dependencies Latest`
- `High Risks Latest`
- `Commitments Due Next 7 Days`
- `Open Commitments`
- `Overdue Commitments`
- `Open Dependencies`
- `High Risks`

## Drillthrough Behavior

- `Initiatives[initiative_name]` selection -> Initiative Detail.
- `Commitments[commitment_id]` row -> Commitment Detail.
- `Dependencies[dependency_id]` row -> Dependency Detail.
- `Risks[risk_id]` row -> Risk Detail.

## Warnings/Limitations

- Do not calculate readiness from open commitments, overdue commitments, dependencies, or risks.
- `Readiness Score Placeholder Latest` and `Risk Score Placeholder Latest` are imported values only.
- Program-level and Executive-level score cards must remain blank unless approved higher-level snapshots exist.
- Activity-derived indicators may appear only through commitments, risks, dependencies, metric snapshots, or source references.
- Owner filtering is object-specific in MVP.

## AI Summary Input Fields

- `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`
- Score placeholder snapshots and notes
- Open and overdue commitment details
- Blocking dependency details
- High and critical risk details
- `MetricSnapshots[threshold_status]` and `MetricSnapshots[source_system]`

---

# Page 4: Dependencies & Risks

## Purpose

Provide an operational view of blockers and threats across Programs and Initiatives.

This page answers:

- What is blocked?
- Which risks require intervention?
- Which areas are causing or experiencing bottlenecks?
- Which Initiatives are at risk due to unresolved dependencies or risks?

## Primary Users

- Operations leadership
- Program managers
- Initiative owners
- Directors
- Executive sponsors

## Filters/Slicers

- `Programs[program_name]`
- `Initiatives[initiative_name]`
- `Dependencies[dependency_type]`
- `Dependencies[blocking_area]`
- `Dependencies[impacted_area]`
- `Dependencies[status]`
- `Dependencies[severity]`
- `Risks[risk_type]`
- `Risks[severity]`
- `Risks[status]`
- `Dependencies[owner]` or `Risks[owner]` as object-specific owner slicers
- `Dependencies[due_date]`
- `Risks[target_resolution_date]`

## KPI Cards

| Card | Measure | Notes |
| --- | --- | --- |
| Open Dependencies | `Open Dependencies` | Current dependency count. |
| Overdue Dependencies | `Overdue Dependencies` | Current overdue dependency count. |
| High Severity Dependencies | `High Severity Dependencies` | Current high-severity unresolved blockers. |
| Open Risks | `Open Risks` | Current unresolved risks. |
| High Risks | `High Risks` | Current unresolved high risks. |
| Critical Risks | `Critical Risks` | Current unresolved critical risks. |
| Initiatives At Risk | `Initiatives At Risk` | Distinct Initiative count. |

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Dependency Blocker Map | Matrix | Rows: `Dependencies[blocking_area]`; Columns: `Dependencies[impacted_area]`; Values: `Open Dependencies`, `High Severity Dependencies` | Identify bottleneck patterns. |
| Risk Severity by Program | Stacked bar | Axis: `Programs[program_name]`; Legend: `Risks[severity]`; Values: count of `Risks[risk_id]` | Compare risk load. |
| Risk Type Mix | Bar or treemap | `Risks[risk_type]`; Values: count of `Risks[risk_id]` | Show major threat categories. |
| Dependency Aging / Due Timeline | Bar by due bucket | Buckets derived from `Dependencies[due_date]`; Values: `Open Dependencies` | Show urgency. |
| Risk Resolution Timeline | Bar by target resolution date | `Risks[target_resolution_date]`; Values: `Open Risks` | Show upcoming risk resolution pressure. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Dependency Register | `Dependencies[dependency_id]`, `Dependencies[dependency_name]`, `Initiatives[initiative_name]`, `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[status]`, `Dependencies[severity]`, `Dependencies[impact_description]`, `Dependencies[resolution_notes]` |
| Risk Register | `Risks[risk_id]`, `Risks[risk_name]`, `Initiatives[initiative_name]`, `Risks[risk_type]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[status]`, `Risks[owner]`, `Risks[date_identified]`, `Risks[target_resolution_date]`, `Risks[mitigation_plan]`, `Risks[source_system]`, `Risks[source_record_id]` |
| At-Risk Initiatives | `Programs[program_name]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `High Severity Dependencies`, `High Risks`, `Critical Risks` |

## Measures Used

- `Open Dependencies`
- `Resolved Dependencies`
- `Overdue Dependencies`
- `High Severity Dependencies`
- `Open Risks`
- `High Risks`
- `Critical Risks`
- `Resolved Risks`
- `Initiatives At Risk`
- `Open Dependencies Latest`
- `High Risks Latest`

## Drillthrough Behavior

- `Dependencies[dependency_id]` row -> Dependency Detail.
- `Risks[risk_id]` row -> Risk Detail.
- `Initiatives[initiative_name]` row -> Initiative Detail.
- `Programs[program_name]` bar -> Program Detail.

## Warnings/Limitations

- Dependencies and Risks link to Initiative, not directly to Program.
- High risks from snapshots and current high risks from the Risks table may differ if snapshot timing differs from current records.
- Source records may point back to CRM or planning systems, but those records remain outside FCC ownership.
- Use `Dependencies[owner]` and `Risks[owner]` separately unless a future `Dim Owner` is added.

## AI Summary Input Fields

- `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[severity]`, `Dependencies[due_date]`, `Dependencies[impact_description]`
- `Risks[severity]`, `Risks[likelihood]`, `Risks[mitigation_plan]`, `Risks[target_resolution_date]`
- `Initiatives[initiative_name]` and `Programs[program_name]`
- `source_system` and `source_record_id` fields for traceability

---

# Page 5: Commitments & Follow-Up

## Purpose

Track accountability, overdue work, due-soon commitments, and follow-up compliance placeholders.

This page answers:

- What commitments are open, due soon, or overdue?
- Who owns the commitments?
- Which Initiatives have execution discipline concerns?
- What follow-up and commitment compliance indicators are available?

## Primary Users

- Initiative owners
- Development officers
- Program managers
- Operations managers
- Directors

## Filters/Slicers

- `Programs[program_name]`
- `Initiatives[initiative_name]`
- `Commitments[owner]` as a Commitment-specific owner slicer
- `Commitments[commitment_type]`
- `Commitments[status]`
- `Commitments[priority]`
- `Commitments[escalation_level]`
- `Commitments[due_date]`
- `Commitments[source_system]`

## KPI Cards

| Card | Measure | Notes |
| --- | --- | --- |
| Open Commitments | `Open Commitments` | Current fact count. |
| Completed Commitments | `Completed Commitments` | Current fact count. |
| Overdue Commitments | `Overdue Commitments` | Derived from due date and status. |
| Due Next 7 Days | `Commitments Due Next 7 Days` | Near-term work queue. |
| Commitment Completion Rate | `Commitment Completion Rate` | Current fact-based completion rate. |
| Follow-Up Compliance Placeholder | `Follow-Up Compliance Placeholder Latest` | Snapshot placeholder/config input. |
| Commitment Compliance Placeholder | `Commitment Compliance Placeholder Latest` | Snapshot placeholder/config input. |

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Commitments by Status | Stacked bar | `Commitments[status]`; Values: count of `Commitments[commitment_id]` | Show accountability state. |
| Overdue by Commitment Owner | Bar chart | Axis: `Commitments[owner]`; Values: `Overdue Commitments` | Identify follow-up/accountability pressure for Commitments only. |
| Due Date Calendar / Timeline | Calendar or bar by week | `Commitments[due_date]`; Values: count of `Commitments[commitment_id]` | Show work coming due. |
| Commitment Type Mix | Bar chart | `Commitments[commitment_type]`; Values: count of `Commitments[commitment_id]` | Show type of obligations. |
| Compliance Placeholder Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend/filter: `follow_up_compliance`, `commitment_compliance`; Values: `MetricSnapshots[metric_value]` | Show imported placeholder trends only. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Commitment Work Queue | `Commitments[commitment_id]`, `Commitments[commitment_name]`, `Initiatives[initiative_name]`, `Commitments[commitment_type]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[value_amount]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]`, `Commitments[notes]` |
| Overdue Commitments | `Commitments[commitment_name]`, `Initiatives[initiative_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |
| Source Traceability | `Commitments[commitment_id]`, `Commitments[source_system]`, `Commitments[source_record_id]`, `Commitments[notes]` |

## Measures Used

- `Open Commitments`
- `Completed Commitments`
- `Overdue Commitments`
- `Commitments Due Next 7 Days`
- `Commitment Completion Rate`
- `Open Commitments Latest`
- `Overdue Commitments Latest`
- `Follow-Up Compliance Placeholder Latest`
- `Commitment Compliance Placeholder Latest`

## Drillthrough Behavior

- `Commitments[commitment_id]` row -> Commitment Detail.
- `Initiatives[initiative_name]` row -> Initiative Detail.
- `Commitments[owner]` selection filters Commitment visuals only in MVP.

## Warnings/Limitations

- Do not show RE NXT Actions, Planner tasks, or other Activities as FCC-owned rows.
- Follow-up compliance is a MetricSnapshot placeholder until approved weighted numerator/denominator inputs exist.
- Commitment completion rate is based on FCC Commitment records, not source-system Activities.
- Source system fields support lineage only.
- Do not use `Commitments[owner]` as a cross-object owner filter until a conformed `Dim Owner` exists.

## AI Summary Input Fields

- Open and overdue commitment details
- Due-next-seven-days commitments
- `Commitments[owner]` and `Commitments[escalation_level]`
- `Commitments[source_system]` and `Commitments[source_record_id]`
- Compliance placeholder snapshots and notes

---

# Page 6: Knowledgebase

## Purpose

Show institutional knowledge assets that support fundraising operations, with ownership, status, review dates, and Initiative/Program context.

This page answers:

- What approved knowledge assets exist?
- Which assets are draft, archived, or due for review?
- Who owns knowledge stewardship?
- Which Initiatives lack supporting knowledge?

## Primary Users

- Operations teams
- Program managers
- Initiative owners
- Knowledge managers
- New staff / onboarding users

## Filters/Slicers

- `Programs[program_name]`
- `Initiatives[initiative_name]`
- `Knowledge[knowledge_type]`
- `Knowledge[status]`
- `Knowledge[source_authority]`
- `Knowledge[owner]` as a Knowledge-specific owner slicer
- `Knowledge[review_date]`
- `Knowledge[tags]`

Knowledge status must remain separate from operational status.

## KPI Cards

These may be implemented as simple counts in the visual layer if DAX measures are not yet defined:

| Card | Field / Future Measure | Notes |
| --- | --- | --- |
| Knowledge Assets | Count of `Knowledge[knowledge_id]` | Total knowledge records in context. |
| Approved Assets | Count filtered to `Knowledge[status] = "Approved"` | Knowledge lifecycle only. |
| Draft Assets | Count filtered to `Knowledge[status] = "Draft"` | Knowledge lifecycle only. |
| Assets Due For Review | Count where `Knowledge[review_date] < TODAY()` | Future DAX measure recommended. |
| Assets Missing Owner | Count blank `Knowledge[owner]` | Future DAX measure recommended. |

Do not reuse operational status measures for Knowledge.

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Knowledge by Program and Initiative | Matrix | Rows: `Programs[program_name]`, `Initiatives[initiative_name]`; Columns: `Knowledge[knowledge_type]`; Values: count of `Knowledge[knowledge_id]` | Show support coverage. |
| Knowledge Status Mix | Bar or donut | `Knowledge[status]`; Values: count of `Knowledge[knowledge_id]` | Show lifecycle state. |
| Review Calendar | Timeline/table | `Knowledge[review_date]`, `Knowledge[title]`, `Knowledge[owner]` | Show upcoming review obligations. |
| Source Authority Mix | Bar chart | `Knowledge[source_authority]`; Values: count of `Knowledge[knowledge_id]` | Distinguish Working, Approved, Official assets. |
| Tag Explorer | Table or slicer | `Knowledge[tags]`, `Knowledge[title]`, `Knowledge[knowledge_type]` | Support search-like navigation. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Knowledge Asset Register | `Knowledge[knowledge_id]`, `Knowledge[title]`, `Knowledge[knowledge_type]`, `Programs[program_name]`, `Initiatives[initiative_name]`, `Knowledge[owner]`, `Knowledge[status]`, `Knowledge[source_authority]`, `Knowledge[review_date]`, `Knowledge[document_link]`, `Knowledge[tags]` |
| Assets Due For Review | `Knowledge[title]`, `Knowledge[knowledge_type]`, `Knowledge[owner]`, `Knowledge[status]`, `Knowledge[source_authority]`, `Knowledge[review_date]`, `Programs[program_name]`, `Initiatives[initiative_name]` |
| Initiative Knowledge Coverage | `Programs[program_name]`, `Initiatives[initiative_name]`, count of `Knowledge[knowledge_id]`, count filtered to `Knowledge[status] = "Approved"`, minimum future `Knowledge[review_date]` |

## Measures Used

Current DAX measure set has no Knowledge-specific measures yet. MVP visuals may use implicit counts of `Knowledge[knowledge_id]` or future explicit measures:

- Knowledge Assets
- Approved Knowledge Assets
- Draft Knowledge Assets
- Assets Due For Review
- Assets Missing Review Owner

Do not use operational measures such as `Open Risks`, `Open Commitments`, or Dim Status as Knowledge lifecycle measures.

## Drillthrough Behavior

- `Knowledge[knowledge_id]` row -> Knowledge Detail.
- `Initiatives[initiative_name]` row -> Initiative Detail.
- `Programs[program_name]` row -> Program Detail.
- `Knowledge[document_link]` opens the SharePoint/knowledge document target when available.

## Warnings/Limitations

- Knowledge is a FCC-managed metadata object, but linked documents may live in SharePoint libraries.
- Knowledge lifecycle status is separate from operational status.
- Do not combine Draft/Approved/Archived into the operational status dimension.
- Some Knowledge assets may have blank Initiative references for organization-wide assets; handle these separately rather than forcing artificial Initiative links.
- `Knowledge[owner]` filters Knowledge visuals only in MVP.

## AI Summary Input Fields

- `Knowledge[title]`, `Knowledge[knowledge_type]`, `Knowledge[status]`, `Knowledge[source_authority]`
- `Knowledge[owner]` and `Knowledge[review_date]`
- `Programs[program_name]` and `Initiatives[initiative_name]`
- `Knowledge[tags]` and `Knowledge[document_link]`
- Related Initiative risks, dependencies, and commitments only when the relationship path is clear

AI may summarize knowledge coverage and review needs. It should not infer document quality or policy approval beyond the stored Knowledge fields.

---

# Cross-Page Warnings

- Do not create Activities visuals as if FCC owns Activities.
- Activity-derived insights may appear only as Metric Snapshots, Commitments, Risks, Dependencies, or source references.
- Do not display Program-level or Executive-level readiness/risk scores unless explicitly supplied as approved higher-level MetricSnapshots.
- Use readiness and risk score placeholders only at Initiative level.
- Do not use a generic `Latest Metric Value` measure.
- Do not merge Knowledge status with operational status.
- Avoid bidirectional filters unless a specific report requirement proves they are necessary.
- Use source fields for lineage, not as relationship keys in the core model.
- MVP owner fields are object-specific. Cross-object owner filtering requires a future conformed `Dim Owner` table.

---

# Recommended MVP Navigation

Suggested page order:

1. Executive Control Tower
2. Work Portfolio
3. Readiness & Execution
4. Dependencies & Risks
5. Commitments & Follow-Up
6. Knowledgebase

Recommended interaction pattern:

- Start at Executive Control Tower.
- Drill into Program or Initiative.
- Move to focused operational pages for Risks, Dependencies, Commitments, or Knowledge.
- Use source system and source record ID only when source traceability is needed.
