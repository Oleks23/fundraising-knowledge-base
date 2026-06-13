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

Filters should flow from Program to Initiative, then from Initiative to child fact tables. Do not create direct Program-to-fact relationships for report convenience.

Metric Snapshot behavior must follow `docs/METRIC_SNAPSHOT_ROLLUP_RULES.md`:

- Count metrics sum across visible Initiatives at the latest snapshot date.
- Compliance metrics use simple average only as an MVP placeholder.
- Readiness and risk score placeholders are Initiative-level only.
- Program-level and Executive-level readiness/risk scores must remain blank unless explicitly supplied as approved higher-level MetricSnapshots.
- Do not use a generic `Latest Metric Value` measure.

---

# Shared Report Filters

Use these common slicers where useful across pages:

| Slicer | Source table | Field |
| --- | --- | --- |
| Program | Programs | `program_name` |
| Initiative | Initiatives | `initiative_name` |
| Initiative Status | Initiatives | `status` |
| Owner | Initiatives, Commitments, Dependencies, Risks, Knowledge | `owner` |
| Department | Programs, Initiatives | `department` |
| Snapshot Date | MetricSnapshots | `snapshot_date` |
| Commitment Type | Commitments | `commitment_type` |
| Risk Type | Risks | `risk_type` |
| Dependency Type | Dependencies | `dependency_type` |
| Source System | source-traceable tables | `source_system` |

Use a dedicated Date table when added to the semantic model. Until then, date slicers may use base table date fields for MVP validation.

---

# Shared Drillthrough Pages

The MVP report should support these drillthrough targets:

| Drillthrough target | Context fields | Purpose |
| --- | --- | --- |
| Initiative Detail | `initiative_id`, `initiative_name` | Show one Initiative with its commitments, dependencies, risks, knowledge, and latest Initiative-level score placeholders. |
| Program Detail | `program_id`, `program_name` | Show all Initiatives and aggregated operational facts for one Program. Do not show Program readiness/risk score unless explicitly supplied. |
| Commitment Detail | `commitment_id` | Show commitment owner, due date, status, source system, source record ID, escalation, and notes. |
| Risk Detail | `risk_id` | Show risk severity, likelihood, owner, mitigation plan, source system, and source record ID. |
| Dependency Detail | `dependency_id` | Show blocker details, impacted area, owner, due date, severity, and resolution notes. |
| Knowledge Detail | `knowledge_id` | Show knowledge asset metadata, review date, owner, status, document link, and tags. |

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

- Program
- Department
- Executive Owner
- Initiative Status
- Snapshot Date
- Source System

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
| Risk Severity Mix | Stacked bar or donut | `Risks[severity]`, count of `Risks[risk_id]` filtered to open/monitoring | Show severity composition. |
| Commitment Status Mix | Stacked bar | `Commitments[status]`, count of `Commitments[commitment_id]` | Show current accountability status. |
| Snapshot Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend: `metric_name`; Values: `metric_value`; filter to count metrics only | Show recent movement for operational counts. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Top Intervention List | Program, Initiative, Owner, Status, `Overdue Commitments`, `High Risks`, `High Severity Dependencies`, target date |
| High/Critical Risks | Risk name, Initiative, Owner, Severity, Likelihood, Target Resolution Date, Source System, Source Record ID |
| Overdue Commitments | Commitment name, Initiative, Owner, Due Date, Priority, Escalation Level, Source System, Source Record ID |

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

- Program bar -> Program Detail.
- Initiative row -> Initiative Detail.
- Risk row -> Risk Detail.
- Commitment row -> Commitment Detail.

## Warnings/Limitations

- Compliance cards are MVP placeholders until numerator/denominator fields exist.
- Executive readiness score must not be displayed unless an approved Executive-level MetricSnapshot exists.
- Snapshot cards reflect latest snapshot data, while current-state tables reflect current fact records; label visuals accordingly.
- Do not add source-system task or activity visuals.

## AI Summary Input Fields

Use these fields for Executive summaries:

- Programs: `program_name`, `executive_owner`, `department`, `status`
- Initiatives: `initiative_name`, `owner`, `status`, `target_date`
- MetricSnapshots: `snapshot_date`, `metric_name`, `metric_value`, `threshold_status`
- Risks: `risk_name`, `severity`, `likelihood`, `status`, `mitigation_plan`, `target_resolution_date`
- Dependencies: `dependency_name`, `severity`, `status`, `impact_description`, `due_date`
- Commitments: `commitment_name`, `owner`, `due_date`, `status`, `priority`, `escalation_level`

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

- Program
- Initiative Status
- Initiative Type
- Owner
- Department
- Target Date range

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
| Initiative Portfolio Matrix | Matrix | Rows: Program, Initiative; Columns/Values: Owner, Status, Target Date, Open Commitments, Open Dependencies, High Risks | Main work inventory. |
| Initiative Status by Program | Stacked bar | Axis: Program; Legend: Initiative Status; Values: Initiative count | Show distribution of active/completed/on-hold work. |
| Owner Workload | Bar chart | Axis: Owner; Values: Active Initiatives, Open Commitments, Open Dependencies, Open Risks | Show accountability concentration. |
| Target Date Timeline | Timeline or bar by month | Axis: Target Date month; Values: Initiative count | Show upcoming portfolio milestones. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Initiative Register | Initiative ID, Initiative Name, Program, Initiative Type, Owner, Department, Status, Start Date, Target Date, Goal Amount, Source System, Source Record ID |
| Portfolio Risk/Execution Summary | Initiative Name, Owner, Open Commitments, Overdue Commitments, Open Dependencies, High Risks, Critical Risks |

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

- Program row -> Program Detail.
- Initiative row -> Initiative Detail.
- Owner selection filters related commitments, dependencies, risks, and knowledge where owner fields are available.

## Warnings/Limitations

- Owner is text in MVP and may not represent a resolved identity dimension yet.
- Program-level scores are intentionally absent.
- Source system fields indicate lineage, not ownership by FCC.

## AI Summary Input Fields

- Program and Initiative identity fields
- Initiative owner, status, department, target date
- Open/overdue counts from Commitments, Dependencies, and Risks
- Source system/source record ID for lineage context

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

- Program
- Initiative
- Initiative Owner
- Initiative Status
- Snapshot Date
- Threshold Status

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
| Initiative Readiness Snapshot | Card group or KPI strip | `Readiness Score Placeholder Latest`, `Risk Score Placeholder Latest`, latest count metrics | Show Initiative-level imported score context. |
| Execution Pressure Trend | Line chart | Axis: `snapshot_date`; Legend: count metric names; Value: `metric_value` | Track counts over time for selected Initiative. |
| Commitments by Due Window | Bar chart | Due buckets derived from `due_date`; Values: count of Commitments | Show near-term execution pressure. |
| Dependencies Blocking Execution | Bar/table | Dependency type, blocking area, severity, due date | Identify blockers. |
| Risks by Type and Severity | Stacked bar | Risk type, severity, count | Show risk drivers. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Readiness Metric Snapshots | Snapshot Date, Initiative, Metric Name, Metric Value, Metric Unit, Threshold Status, Source System, Notes |
| Execution Commitments | Commitment Name, Owner, Due Date, Status, Priority, Escalation Level, Source System, Source Record ID |
| Blocking Dependencies | Dependency Name, Dependency Type, Blocking Area, Impacted Area, Owner, Due Date, Status, Severity, Impact Description |
| Readiness Risks | Risk Name, Risk Type, Severity, Likelihood, Owner, Status, Mitigation Plan, Target Resolution Date |

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

- Initiative selection -> Initiative Detail.
- Commitment row -> Commitment Detail.
- Dependency row -> Dependency Detail.
- Risk row -> Risk Detail.

## Warnings/Limitations

- Do not calculate readiness from open commitments, overdue commitments, dependencies, or risks.
- `Readiness Score Placeholder Latest` and `Risk Score Placeholder Latest` are imported values only.
- Program-level and Executive-level score cards must remain blank unless approved higher-level snapshots exist.
- Activity-derived indicators may appear only through commitments, risks, dependencies, metric snapshots, or source references.

## AI Summary Input Fields

- Initiative identity, owner, status, target date
- Score placeholder snapshots and notes
- Open and overdue commitment details
- Blocking dependency details
- High and critical risk details
- Threshold status and source system fields from MetricSnapshots

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

- Program
- Initiative
- Dependency Type
- Blocking Area
- Impacted Area
- Dependency Status
- Dependency Severity
- Risk Type
- Risk Severity
- Risk Status
- Owner
- Due Date / Target Resolution Date range

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
| Dependency Blocker Map | Matrix | Rows: Blocking Area; Columns: Impacted Area; Values: Open Dependencies / High Severity Dependencies | Identify bottleneck patterns. |
| Risk Severity by Program | Stacked bar | Axis: Program; Legend: Severity; Values: Risk count | Compare risk load. |
| Risk Type Mix | Bar or treemap | Risk Type; Risk count | Show major threat categories. |
| Dependency Aging / Due Timeline | Bar by due bucket | Due Date bucket; Values: Open Dependencies | Show urgency. |
| Risk Resolution Timeline | Bar by target resolution date | Target Resolution Date; Values: Open Risks | Show upcoming risk resolution pressure. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Dependency Register | Dependency ID, Dependency Name, Initiative, Dependency Type, Blocking Area, Impacted Area, Owner, Due Date, Status, Severity, Impact Description, Resolution Notes |
| Risk Register | Risk ID, Risk Name, Initiative, Risk Type, Severity, Likelihood, Status, Owner, Date Identified, Target Resolution Date, Mitigation Plan, Source System, Source Record ID |
| At-Risk Initiatives | Program, Initiative, Owner, Status, High Severity Dependencies, High Risks, Critical Risks |

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

- Dependency row -> Dependency Detail.
- Risk row -> Risk Detail.
- Initiative row -> Initiative Detail.
- Program bar -> Program Detail.

## Warnings/Limitations

- Dependencies and Risks link to Initiative, not directly to Program.
- High risks from snapshots and current high risks from the Risks table may differ if snapshot timing differs from current records.
- Source records may point back to CRM or planning systems, but those records remain outside FCC ownership.

## AI Summary Input Fields

- Dependency blocker/impacted areas, severity, due date, impact description
- Risk severity, likelihood, mitigation plan, target resolution date
- Initiative and Program context
- Source system and source record ID for traceability

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

- Program
- Initiative
- Owner
- Commitment Type
- Commitment Status
- Priority
- Escalation Level
- Due Date range
- Source System

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
| Commitments by Status | Stacked bar | Status; count of Commitments | Show accountability state. |
| Overdue by Owner | Bar chart | Owner; `Overdue Commitments` | Identify follow-up/accountability pressure. |
| Due Date Calendar / Timeline | Calendar or bar by week | Due Date; count of Commitments | Show work coming due. |
| Commitment Type Mix | Bar chart | Commitment Type; count of Commitments | Show type of obligations. |
| Compliance Placeholder Trend | Line chart | Snapshot Date; `follow_up_compliance`, `commitment_compliance` values | Show imported placeholder trends only. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Commitment Work Queue | Commitment ID, Commitment Name, Initiative, Commitment Type, Owner, Due Date, Status, Priority, Value Amount, Escalation Level, Source System, Source Record ID, Notes |
| Overdue Commitments | Commitment Name, Initiative, Owner, Due Date, Priority, Escalation Level, Source System, Source Record ID |
| Source Traceability | Commitment ID, Source System, Source Record ID, Notes |

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

- Commitment row -> Commitment Detail.
- Initiative row -> Initiative Detail.
- Owner selection cross-filters Commitments, Risks, and Dependencies where owner fields match.

## Warnings/Limitations

- Do not show RE NXT Actions, Planner tasks, or other Activities as FCC-owned rows.
- Follow-up compliance is a MetricSnapshot placeholder until approved weighted numerator/denominator inputs exist.
- Commitment completion rate is based on FCC Commitment records, not source-system Activities.
- Source system fields support lineage only.

## AI Summary Input Fields

- Open and overdue commitment details
- Due-next-seven-days commitments
- Commitment owners and escalation levels
- Source system and source record ID
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

- Program
- Initiative
- Knowledge Type
- Knowledge Status
- Source Authority
- Owner
- Review Date range
- Tags

Knowledge status must remain separate from operational status.

## KPI Cards

These may be implemented as simple counts in the visual layer if DAX measures are not yet defined:

| Card | Field / Future Measure | Notes |
| --- | --- | --- |
| Knowledge Assets | Count of `Knowledge[knowledge_id]` | Total knowledge records in context. |
| Approved Assets | Count filtered to `Knowledge[status] = "Approved"` | Knowledge lifecycle only. |
| Draft Assets | Count filtered to `Knowledge[status] = "Draft"` | Knowledge lifecycle only. |
| Assets Due For Review | Count where `review_date < TODAY()` | Future DAX measure recommended. |
| Assets Missing Owner | Count blank owner | Future DAX measure recommended. |

Do not reuse operational status measures for Knowledge.

## Core Visuals

| Visual | Type | Fields / Measures | Purpose |
| --- | --- | --- | --- |
| Knowledge by Program and Initiative | Matrix | Program, Initiative, Knowledge Type, count of Knowledge ID | Show support coverage. |
| Knowledge Status Mix | Bar or donut | Knowledge Status; count of Knowledge ID | Show lifecycle state. |
| Review Calendar | Timeline/table | Review Date; Knowledge Title; Owner | Show upcoming review obligations. |
| Source Authority Mix | Bar chart | Source Authority; count of Knowledge ID | Distinguish Working, Approved, Official assets. |
| Tag Explorer | Table or slicer | Tags, Title, Knowledge Type | Support search-like navigation. |

## Table Visuals

| Table | Fields |
| --- | --- |
| Knowledge Asset Register | Knowledge ID, Title, Knowledge Type, Program, Initiative, Owner, Status, Source Authority, Review Date, Document Link, Tags |
| Assets Due For Review | Title, Knowledge Type, Owner, Status, Source Authority, Review Date, Program, Initiative |
| Initiative Knowledge Coverage | Program, Initiative, Knowledge Asset Count, Approved Asset Count, Next Review Date |

## Measures Used

Current DAX measure set has no Knowledge-specific measures yet. MVP visuals may use implicit counts of `Knowledge[knowledge_id]` or future explicit measures:

- Knowledge Assets
- Approved Knowledge Assets
- Draft Knowledge Assets
- Assets Due For Review
- Assets Missing Review Owner

Do not use operational measures such as `Open Risks`, `Open Commitments`, or Dim Status as Knowledge lifecycle measures.

## Drillthrough Behavior

- Knowledge row -> Knowledge Detail.
- Initiative row -> Initiative Detail.
- Program row -> Program Detail.
- Document link opens the SharePoint/knowledge document target when available.

## Warnings/Limitations

- Knowledge is a FCC-managed metadata object, but linked documents may live in SharePoint libraries.
- Knowledge lifecycle status is separate from operational status.
- Do not combine Draft/Approved/Archived into the operational status dimension.
- Some Knowledge assets may have blank Initiative references for organization-wide assets; handle these separately rather than forcing artificial Initiative links.

## AI Summary Input Fields

- Knowledge title, type, status, source authority
- Owner and review date
- Program and Initiative context
- Tags and document link
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
