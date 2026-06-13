# Power BI Wireframe Specs

# Fundraising Command Centre (FCC)

Version: 1.0

---

# Purpose

This document translates the MVP Power BI page specifications into implementation-ready wireframe guidance for a 16:9 report canvas.

The wireframes use the Sprint 2 model objects and the current DAX measures in `powerbi/dax/core_measures.dax`. They do not introduce an Activities page, Activities visuals, unsupported Program/Executive readiness rollups, or a conformed Owner slicer.

---

# Global Canvas Standard

Use a 16:9 Power BI report canvas.

Recommended zone pattern:

| Zone | Approximate canvas position | Purpose |
| --- | --- | --- |
| Header | Top 8-10% | Page title, subtitle, last snapshot/reference date, navigation buttons. |
| Slicer rail | Left 15-18% or top below header | Page-specific filters. Use object-specific owner fields. |
| KPI strip | Top body row, 12-18% height | Primary cards. |
| Main visual area | Center body, 40-50% height | Main management visuals. |
| Detail table area | Bottom body, 25-35% height | Intervention lists, registers, and drillthrough source rows. |
| Warnings/notes | Bottom corner or hidden tooltip | MVP limitations and placeholder labels. |

Use single-direction filtering through the documented relationship path:

```text
Programs[program_id]
  -> Initiatives[program]
      -> child fact tables by initiative
```

---

# Global Constraints

- Do not create an Activities page.
- Do not present source activity data as FCC-owned rows.
- Activity-derived insights may appear only as Commitments, Risks, Dependencies, MetricSnapshots, or source references.
- Do not display Program-level or Executive-level readiness/risk scores unless explicitly supplied by approved higher-level MetricSnapshots.
- Use `Readiness Score Placeholder Latest` and `Risk Score Placeholder Latest` only at Initiative context.
- Do not use a generic `Latest Metric Value` card or visual.
- Do not use a conformed Owner slicer in MVP.
- Owner slicers and visuals must be object-specific, such as `Initiatives[owner]`, `Commitments[owner]`, `Risks[owner]`, `Dependencies[owner]`, or `Knowledge[owner]`.
- Any cross-object owner workload element must be labeled future-after-Dim-Owner.
- Use existing DAX measures only unless a measure is explicitly labeled `future measure`.

---

# Drillthrough Targets

| Target | Drillthrough field(s) | Used from pages |
| --- | --- | --- |
| Program Detail | `Programs[program_id]`, `Programs[program_name]` | Executive Control Tower, Work Portfolio, Dependencies & Risks, Knowledgebase |
| Initiative Detail | `Initiatives[initiative_id]`, `Initiatives[initiative_name]` | All pages except pure Program interactions |
| Commitment Detail | `Commitments[commitment_id]` | Executive Control Tower, Readiness & Execution, Commitments & Follow-Up |
| Risk Detail | `Risks[risk_id]` | Executive Control Tower, Readiness & Execution, Dependencies & Risks |
| Dependency Detail | `Dependencies[dependency_id]` | Readiness & Execution, Dependencies & Risks |
| Knowledge Detail | `Knowledge[knowledge_id]` | Knowledgebase |

---

# Page 1: Executive Control Tower

## Page Purpose

Give leadership a five-minute view of what is at risk, overdue, blocked, or requiring intervention across the fundraising portfolio.

## 16:9 Layout Zones

| Zone | Placement | Contents |
| --- | --- | --- |
| Header | Top full width | Title: Executive Control Tower. Subtitle: portfolio health by Program and Initiative. Display `Latest Snapshot Date`. |
| Slicer rail | Left vertical rail | Program, Department, Executive Owner, Initiative Status, Snapshot Date. |
| KPI strip | Top body, right of slicer rail | 8-9 KPI cards in two rows if needed. |
| Main visual grid | Middle body | Program Operational Load, Initiatives Requiring Intervention, Risk Severity Mix. |
| Detail tables | Bottom body | High/Critical Risks and Overdue Commitments. |
| Notes | Bottom right | Placeholder and no-readiness-rollup warning. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Filters through Initiative relationship path. |
| Department | `Programs[department]` | Program-level department view. |
| Executive Owner | `Programs[executive_owner]` | Program owner only; not a conformed Owner slicer. |
| Initiative Status | `Initiatives[status]` | Initiative lifecycle only. |
| Snapshot Date | `MetricSnapshots[snapshot_date]` | Use for snapshot visuals/cards. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Active Initiatives | `Active Initiatives` | Neutral. |
| Open Commitments | `Open Commitments Latest` | Warning if > 0; critical if above locally configured threshold. |
| Overdue Commitments | `Overdue Commitments Latest` | Critical if > 0. |
| Open Dependencies | `Open Dependencies Latest` | Warning if > 0. |
| High Risks | `High Risks Latest` | Critical if > 0. |
| Critical Risks | `Critical Risks` | Critical if > 0. |
| Initiatives At Risk | `Initiatives At Risk` | Critical if > 0. |
| Follow-Up Compliance Placeholder | `Follow-Up Compliance Placeholder Latest` | Label as placeholder/config input. Use muted styling if blank. |
| Commitment Compliance Placeholder | `Commitment Compliance Placeholder Latest` | Label as placeholder/config input. Use muted styling if blank. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Program Operational Load | Clustered bar | Axis: `Programs[program_name]`; Values: `Open Commitments Latest`, `Overdue Commitments Latest`, `Open Dependencies Latest`, `High Risks Latest` | Sort by combined operational burden descending. |
| Initiatives Requiring Intervention | Ranked bar or matrix | `Initiatives[initiative_name]`; Values: `Overdue Commitments`, `High Risks`, `High Severity Dependencies` | Use conditional color for nonzero values. |
| Risk Severity Mix | Stacked bar or donut | Legend: `Risks[severity]`; Values: count of `Risks[risk_id]`; visual filter `Risks[status] <> "Resolved"` | Critical/high colors should stand out. |
| Commitment Status Mix | Stacked bar | Axis/legend: `Commitments[status]`; Values: count of `Commitments[commitment_id]` | Keep commitment status separate from Knowledge status. |
| Count Snapshot Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend: `MetricSnapshots[metric_name]`; Values: `MetricSnapshots[metric_value]`; visual filter metric names to count metrics | Do not include score placeholders in this trend. |

## Tables

| Table | Fields |
| --- | --- |
| Top Intervention List | `Programs[program_name]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`, `Overdue Commitments`, `High Risks`, `High Severity Dependencies` |
| High/Critical Risks | `Risks[risk_id]`, `Risks[risk_name]`, `Initiatives[initiative_name]`, `Risks[owner]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[target_resolution_date]`, `Risks[source_system]`, `Risks[source_record_id]` |
| Overdue Commitments | `Commitments[commitment_id]`, `Commitments[commitment_name]`, `Initiatives[initiative_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |

## Drillthrough Targets

- `Programs[program_name]` -> Program Detail.
- `Initiatives[initiative_name]` -> Initiative Detail.
- `Risks[risk_id]` -> Risk Detail.
- `Commitments[commitment_id]` -> Commitment Detail.

## Warnings/Limitations

- Do not show Executive readiness/risk score cards in MVP.
- Compliance cards are placeholders until numerator/denominator fields exist.
- `Programs[executive_owner]` is Program-specific and does not filter child object owners.
- Snapshot cards and current-state tables may differ because they have different grains/timing.

---

# Page 2: Work Portfolio

## Page Purpose

Show the managed portfolio of Programs and Initiatives, with ownership, status, target dates, and operational load.

## 16:9 Layout Zones

| Zone | Placement | Contents |
| --- | --- | --- |
| Header | Top full width | Title: Work Portfolio. Subtitle: Programs, Initiatives, ownership, and execution load. |
| Slicer rail | Left vertical rail | Program, Initiative Status, Initiative Type, Initiative Owner, Department, Target Date. |
| KPI strip | Top body | Active/Completed Initiatives, Initiatives At Risk, Open Commitments, Open Dependencies, Open Risks. |
| Main visual area | Middle body | Initiative Portfolio Matrix and status/owner visuals. |
| Detail table area | Bottom body | Initiative Register and Portfolio Risk/Execution Summary. |
| Notes | Bottom right | Owner-dimension limitation. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter. |
| Initiative Status | `Initiatives[status]` | Initiative lifecycle only. |
| Initiative Type | `Initiatives[initiative_type]` | Initiative categorization. |
| Initiative Owner | `Initiatives[owner]` | Object-specific owner slicer. |
| Department | `Initiatives[department]` | Initiative-level department view. |
| Target Date | `Initiatives[target_date]` | Use date range or relative slicer. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Active Initiatives | `Active Initiatives` | Neutral. |
| Completed Initiatives | `Completed Initiatives` | Neutral/success. |
| Initiatives At Risk | `Initiatives At Risk` | Critical if > 0. |
| Open Commitments | `Open Commitments` | Warning if > 0. |
| Open Dependencies | `Open Dependencies` | Warning if > 0. |
| Open Risks | `Open Risks` | Warning if > 0; critical when high/critical risk visuals indicate severe risk. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Initiative Portfolio Matrix | Matrix | Rows: `Programs[program_name]`, `Initiatives[initiative_name]`; Values: `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`, `Open Commitments`, `Open Dependencies`, `High Risks` | Primary portfolio scan. |
| Initiative Status by Program | Stacked bar | Axis: `Programs[program_name]`; Legend: `Initiatives[status]`; Values: count of `Initiatives[initiative_id]` | Show portfolio lifecycle distribution. |
| Initiative Owner Workload | Bar chart | Axis: `Initiatives[owner]`; Values: `Active Initiatives` | MVP object-specific owner view. |
| Future Conformed Owner Workload | Do not build in MVP | Future axis: `Dim Owner`; Values: Active Initiatives, Open Commitments, Open Dependencies, Open Risks | Label future-after-Dim-Owner only if shown in documentation. |
| Target Date Timeline | Bar by month | Axis: month from `Initiatives[target_date]`; Values: count of `Initiatives[initiative_id]` | Date table recommended later. |

## Tables

| Table | Fields |
| --- | --- |
| Initiative Register | `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Programs[program_name]`, `Initiatives[initiative_type]`, `Initiatives[owner]`, `Initiatives[department]`, `Initiatives[status]`, `Initiatives[start_date]`, `Initiatives[target_date]`, `Initiatives[goal_amount]`, `Initiatives[source_system]`, `Initiatives[source_record_id]` |
| Portfolio Risk/Execution Summary | `Initiatives[initiative_name]`, `Initiatives[owner]`, `Open Commitments`, `Overdue Commitments`, `Open Dependencies`, `High Risks`, `Critical Risks`, `High Severity Dependencies` |

## Drillthrough Targets

- `Programs[program_name]` -> Program Detail.
- `Initiatives[initiative_name]` -> Initiative Detail.

## Warnings/Limitations

- Do not use `Average Readiness Score` or `Average Risk Score` for Program-level portfolio cards.
- `Initiatives[owner]` filters Initiative visuals only in MVP.
- Cross-object owner workload requires future `Dim Owner`.

---

# Page 3: Readiness & Execution

## Page Purpose

Show Initiative-level readiness inputs and execution pressure without inventing readiness or risk scoring formulas.

## 16:9 Layout Zones

| Zone | Placement | Contents |
| --- | --- | --- |
| Header | Top full width | Title: Readiness & Execution. Subtitle: Initiative-level imported scores and execution signals. |
| Slicer rail | Left vertical rail | Program, Initiative, Initiative Owner, Initiative Status, Snapshot Date, Threshold Status. |
| KPI strip | Top body | Initiative-level score placeholders plus latest count metrics. |
| Main visual area | Middle body | Execution Pressure Trend, Due Window, Dependency and Risk visuals. |
| Detail table area | Bottom body | Metric snapshots, execution commitments, blocking dependencies, readiness risks. |
| Notes | Bottom right | Score placeholder warning. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter. |
| Initiative | `Initiatives[initiative_name]` | Required for score placeholder cards. |
| Initiative Owner | `Initiatives[owner]` | Object-specific owner slicer. |
| Initiative Status | `Initiatives[status]` | Initiative lifecycle only. |
| Snapshot Date | `MetricSnapshots[snapshot_date]` | Snapshot filter. |
| Threshold Status | `MetricSnapshots[threshold_status]` | Snapshot threshold view. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Readiness Score Placeholder | `Readiness Score Placeholder Latest` | Show only with Initiative context; muted/blank otherwise. |
| Risk Score Placeholder | `Risk Score Placeholder Latest` | Show only with Initiative context; muted/blank otherwise. |
| Open Commitments | `Open Commitments Latest` | Warning if > 0. |
| Overdue Commitments | `Overdue Commitments Latest` | Critical if > 0. |
| Open Dependencies | `Open Dependencies Latest` | Warning if > 0. |
| High Risks | `High Risks Latest` | Critical if > 0. |
| Due Next 7 Days | `Commitments Due Next 7 Days` | Warning if > 0. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Initiative Readiness Snapshot | KPI/card group | `Readiness Score Placeholder Latest`, `Risk Score Placeholder Latest`, `Open Commitments Latest`, `Overdue Commitments Latest`, `Open Dependencies Latest`, `High Risks Latest` | Keep scores Initiative-only. |
| Execution Pressure Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend: `MetricSnapshots[metric_name]`; Value: `MetricSnapshots[metric_value]`; filter to count metrics | Do not trend score placeholders as Program rollups. |
| Commitments by Due Window | Bar chart | Buckets from `Commitments[due_date]`; Values: count of `Commitments[commitment_id]` | Suggested buckets: Overdue, 0-7 days, 8-30 days, later. |
| Dependencies Blocking Execution | Bar/table | `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[severity]`, `Dependencies[due_date]` | Highlight high severity and overdue. |
| Risks by Type and Severity | Stacked bar | Axis: `Risks[risk_type]`; Legend: `Risks[severity]`; Values: count of `Risks[risk_id]` | Filter out resolved risks for active risk view. |

## Tables

| Table | Fields |
| --- | --- |
| Readiness Metric Snapshots | `MetricSnapshots[snapshot_date]`, `Initiatives[initiative_name]`, `MetricSnapshots[metric_name]`, `MetricSnapshots[metric_value]`, `MetricSnapshots[metric_unit]`, `MetricSnapshots[threshold_status]`, `MetricSnapshots[source_system]`, `MetricSnapshots[notes]` |
| Execution Commitments | `Commitments[commitment_id]`, `Commitments[commitment_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |
| Blocking Dependencies | `Dependencies[dependency_id]`, `Dependencies[dependency_name]`, `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[status]`, `Dependencies[severity]`, `Dependencies[impact_description]` |
| Readiness Risks | `Risks[risk_id]`, `Risks[risk_name]`, `Risks[risk_type]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[owner]`, `Risks[status]`, `Risks[mitigation_plan]`, `Risks[target_resolution_date]` |

## Drillthrough Targets

- `Initiatives[initiative_name]` -> Initiative Detail.
- `Commitments[commitment_id]` -> Commitment Detail.
- `Dependencies[dependency_id]` -> Dependency Detail.
- `Risks[risk_id]` -> Risk Detail.

## Warnings/Limitations

- Do not calculate readiness from commitments, dependencies, or risks.
- Do not display Program/Executive readiness or risk score rollups.
- Activity-derived execution signals appear only through FCC-owned Commitments/Risks/Dependencies or MetricSnapshots.
- `Initiatives[owner]` is object-specific.

---

# Page 4: Dependencies & Risks

## Page Purpose

Show blockers and threats requiring intervention across Initiatives and Programs.

## 16:9 Layout Zones

| Zone | Placement | Contents |
| --- | --- | --- |
| Header | Top full width | Title: Dependencies & Risks. Subtitle: blockers, risks, and intervention queue. |
| Slicer rail | Left vertical rail | Program, Initiative, dependency filters, risk filters, object-specific owner slicers. |
| KPI strip | Top body | Dependency and Risk cards. |
| Main visual area | Middle body | Blocker map, Risk Severity by Program, Risk Type Mix, timelines. |
| Detail table area | Bottom body | Dependency Register, Risk Register, At-Risk Initiatives. |
| Notes | Bottom right | Snapshot/current-state timing note. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter. |
| Initiative | `Initiatives[initiative_name]` | Shared Initiative filter. |
| Dependency Type | `Dependencies[dependency_type]` | Dependency-specific. |
| Blocking Area | `Dependencies[blocking_area]` | Dependency-specific. |
| Impacted Area | `Dependencies[impacted_area]` | Dependency-specific. |
| Dependency Status | `Dependencies[status]` | Dependency-specific. |
| Dependency Severity | `Dependencies[severity]` | Dependency-specific. |
| Risk Type | `Risks[risk_type]` | Risk-specific. |
| Risk Severity | `Risks[severity]` | Risk-specific. |
| Risk Status | `Risks[status]` | Risk-specific. |
| Dependency Owner | `Dependencies[owner]` | Object-specific owner slicer. |
| Risk Owner | `Risks[owner]` | Object-specific owner slicer. |
| Dependency Due Date | `Dependencies[due_date]` | Date table recommended later. |
| Risk Target Resolution Date | `Risks[target_resolution_date]` | Date table recommended later. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Open Dependencies | `Open Dependencies` | Warning if > 0. |
| Overdue Dependencies | `Overdue Dependencies` | Critical if > 0. |
| High Severity Dependencies | `High Severity Dependencies` | Critical if > 0. |
| Open Risks | `Open Risks` | Warning if > 0. |
| High Risks | `High Risks` | Critical if > 0. |
| Critical Risks | `Critical Risks` | Critical if > 0. |
| Initiatives At Risk | `Initiatives At Risk` | Critical if > 0. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Dependency Blocker Map | Matrix | Rows: `Dependencies[blocking_area]`; Columns: `Dependencies[impacted_area]`; Values: `Open Dependencies`, `High Severity Dependencies` | Conditional color for high severity. |
| Risk Severity by Program | Stacked bar | Axis: `Programs[program_name]`; Legend: `Risks[severity]`; Values: count of `Risks[risk_id]` | Filter out resolved risks for active view. |
| Risk Type Mix | Bar or treemap | `Risks[risk_type]`; Values: count of `Risks[risk_id]` | Highlight High/Critical with tooltip. |
| Dependency Due Timeline | Bar by due bucket | Buckets from `Dependencies[due_date]`; Values: `Open Dependencies` | Critical for overdue. |
| Risk Resolution Timeline | Bar by date | Axis: `Risks[target_resolution_date]`; Values: `Open Risks` | Show upcoming resolution pressure. |

## Tables

| Table | Fields |
| --- | --- |
| Dependency Register | `Dependencies[dependency_id]`, `Dependencies[dependency_name]`, `Initiatives[initiative_name]`, `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[status]`, `Dependencies[severity]`, `Dependencies[impact_description]`, `Dependencies[resolution_notes]` |
| Risk Register | `Risks[risk_id]`, `Risks[risk_name]`, `Initiatives[initiative_name]`, `Risks[risk_type]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[status]`, `Risks[owner]`, `Risks[date_identified]`, `Risks[target_resolution_date]`, `Risks[mitigation_plan]`, `Risks[source_system]`, `Risks[source_record_id]` |
| At-Risk Initiatives | `Programs[program_name]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `High Severity Dependencies`, `High Risks`, `Critical Risks` |

## Drillthrough Targets

- `Dependencies[dependency_id]` -> Dependency Detail.
- `Risks[risk_id]` -> Risk Detail.
- `Initiatives[initiative_name]` -> Initiative Detail.
- `Programs[program_name]` -> Program Detail.

## Warnings/Limitations

- Use `Dependencies[owner]` and `Risks[owner]` separately.
- Risks and Dependencies reach Program only through Initiative.
- Snapshot high-risk counts may differ from current `Risks` records if refresh timing differs.
- Source fields are lineage only.

---

# Page 5: Commitments & Follow-Up

## Page Purpose

Track obligations, overdue work, due-soon commitments, and imported compliance placeholders.

## 16:9 Layout Zones

| Zone | Placement | Contents |
| --- | --- | --- |
| Header | Top full width | Title: Commitments & Follow-Up. Subtitle: accountability, deadlines, and compliance placeholders. |
| Slicer rail | Left vertical rail | Program, Initiative, Commitment Owner, Type, Status, Priority, Escalation, Due Date, Source System. |
| KPI strip | Top body | Commitment count/rate cards and compliance placeholders. |
| Main visual area | Middle body | Status, owner, due date, type, and compliance trend charts. |
| Detail table area | Bottom body | Commitment Work Queue, Overdue Commitments, Source Traceability. |
| Notes | Bottom right | Compliance placeholder and no-Activities warning. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter. |
| Initiative | `Initiatives[initiative_name]` | Shared Initiative filter. |
| Commitment Owner | `Commitments[owner]` | Commitment-specific owner slicer. |
| Commitment Type | `Commitments[commitment_type]` | Commitment-specific. |
| Commitment Status | `Commitments[status]` | Commitment lifecycle only. |
| Priority | `Commitments[priority]` | Commitment-specific. |
| Escalation Level | `Commitments[escalation_level]` | Commitment-specific. |
| Commitment Due Date | `Commitments[due_date]` | Date table recommended later. |
| Source System | `Commitments[source_system]` | Lineage filter only. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Open Commitments | `Open Commitments` | Warning if > 0. |
| Completed Commitments | `Completed Commitments` | Success/neutral. |
| Overdue Commitments | `Overdue Commitments` | Critical if > 0. |
| Due Next 7 Days | `Commitments Due Next 7 Days` | Warning if > 0. |
| Commitment Completion Rate | `Commitment Completion Rate` | Use percentage format. |
| Follow-Up Compliance Placeholder | `Follow-Up Compliance Placeholder Latest` | Label placeholder/config input. |
| Commitment Compliance Placeholder | `Commitment Compliance Placeholder Latest` | Label placeholder/config input. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Commitments by Status | Stacked bar | Axis/legend: `Commitments[status]`; Values: count of `Commitments[commitment_id]` | Do not merge with Knowledge status. |
| Overdue by Commitment Owner | Bar chart | Axis: `Commitments[owner]`; Values: `Overdue Commitments` | Commitment-owner only. |
| Due Date Calendar / Timeline | Calendar or weekly bar | Axis: `Commitments[due_date]`; Values: count of `Commitments[commitment_id]` | Highlight overdue and next 7 days. |
| Commitment Type Mix | Bar chart | Axis: `Commitments[commitment_type]`; Values: count of `Commitments[commitment_id]` | Show obligation categories. |
| Compliance Placeholder Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Values: `MetricSnapshots[metric_value]`; filter `MetricSnapshots[metric_name]` to `follow_up_compliance`, `commitment_compliance` | Placeholder only; no Activities calculation. |

## Tables

| Table | Fields |
| --- | --- |
| Commitment Work Queue | `Commitments[commitment_id]`, `Commitments[commitment_name]`, `Initiatives[initiative_name]`, `Commitments[commitment_type]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[value_amount]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]`, `Commitments[notes]` |
| Overdue Commitments | `Commitments[commitment_name]`, `Initiatives[initiative_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |
| Source Traceability | `Commitments[commitment_id]`, `Commitments[source_system]`, `Commitments[source_record_id]`, `Commitments[notes]` |

## Drillthrough Targets

- `Commitments[commitment_id]` -> Commitment Detail.
- `Initiatives[initiative_name]` -> Initiative Detail.

## Warnings/Limitations

- Do not show source Activities as FCC-owned commitments.
- Compliance placeholders do not calculate from RE NXT Actions or Planner tasks.
- `Commitments[owner]` is not a cross-object Owner dimension.

---

# Page 6: Knowledgebase

## Page Purpose

Show institutional knowledge assets, review obligations, ownership, lifecycle status, and Initiative/Program coverage.

## 16:9 Layout Zones

| Zone | Placement | Contents |
| --- | --- | --- |
| Header | Top full width | Title: Knowledgebase. Subtitle: knowledge coverage, status, and review stewardship. |
| Slicer rail | Left vertical rail | Program, Initiative, Knowledge Type, Knowledge Status, Source Authority, Knowledge Owner, Review Date, Tags. |
| KPI strip | Top body | Knowledge asset counts, using implicit counts or future measures. |
| Main visual area | Middle body | Knowledge by Program/Initiative, status mix, review calendar, source authority mix. |
| Detail table area | Bottom body | Knowledge Asset Register, Assets Due For Review, Initiative Knowledge Coverage. |
| Notes | Bottom right | Knowledge status is separate from operational status. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter. |
| Initiative | `Initiatives[initiative_name]` | Optional; some Knowledge may be organization-wide. |
| Knowledge Type | `Knowledge[knowledge_type]` | Knowledge-specific. |
| Knowledge Status | `Knowledge[status]` | Separate from operational status. |
| Source Authority | `Knowledge[source_authority]` | Knowledge governance field. |
| Knowledge Owner | `Knowledge[owner]` | Knowledge-specific owner slicer. |
| Review Date | `Knowledge[review_date]` | Date table recommended later. |
| Tags | `Knowledge[tags]` | Text/tag filter. |

## KPI Cards

| Card | Measure / field | Conditional formatting |
| --- | --- | --- |
| Knowledge Assets | Count of `Knowledge[knowledge_id]` | Existing implicit count. |
| Approved Assets | Count of `Knowledge[knowledge_id]` filtered to `Knowledge[status] = "Approved"` | Existing implicit count. |
| Draft Assets | Count of `Knowledge[knowledge_id]` filtered to `Knowledge[status] = "Draft"` | Existing implicit count. |
| Assets Due For Review | Future measure | Warning if > 0; define later. |
| Assets Missing Owner | Future measure | Warning if > 0; define later. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Knowledge by Program and Initiative | Matrix | Rows: `Programs[program_name]`, `Initiatives[initiative_name]`; Columns: `Knowledge[knowledge_type]`; Values: count of `Knowledge[knowledge_id]` | Do not force blank Initiative Knowledge into artificial Initiative. |
| Knowledge Status Mix | Bar or donut | `Knowledge[status]`; Values: count of `Knowledge[knowledge_id]` | Keep separate from operational status. |
| Review Calendar | Timeline/table | `Knowledge[review_date]`, `Knowledge[title]`, `Knowledge[owner]` | Highlight overdue review dates. |
| Source Authority Mix | Bar chart | `Knowledge[source_authority]`; Values: count of `Knowledge[knowledge_id]` | Shows Working/Approved/Official. |
| Tag Explorer | Table/slicer | `Knowledge[tags]`, `Knowledge[title]`, `Knowledge[knowledge_type]` | Supports navigation. |

## Tables

| Table | Fields |
| --- | --- |
| Knowledge Asset Register | `Knowledge[knowledge_id]`, `Knowledge[title]`, `Knowledge[knowledge_type]`, `Programs[program_name]`, `Initiatives[initiative_name]`, `Knowledge[owner]`, `Knowledge[status]`, `Knowledge[source_authority]`, `Knowledge[review_date]`, `Knowledge[document_link]`, `Knowledge[tags]` |
| Assets Due For Review | `Knowledge[title]`, `Knowledge[knowledge_type]`, `Knowledge[owner]`, `Knowledge[status]`, `Knowledge[source_authority]`, `Knowledge[review_date]`, `Programs[program_name]`, `Initiatives[initiative_name]` |
| Initiative Knowledge Coverage | `Programs[program_name]`, `Initiatives[initiative_name]`, count of `Knowledge[knowledge_id]`, count filtered to `Knowledge[status] = "Approved"`, minimum future `Knowledge[review_date]` |

## Drillthrough Targets

- `Knowledge[knowledge_id]` -> Knowledge Detail.
- `Initiatives[initiative_name]` -> Initiative Detail.
- `Programs[program_name]` -> Program Detail.
- `Knowledge[document_link]` -> SharePoint/knowledge document target when available.

## Warnings/Limitations

- Current DAX has no Knowledge-specific explicit measures; use implicit counts or future measures as labeled.
- `Knowledge[status]` is not operational status.
- `Knowledge[owner]` filters Knowledge visuals only.
- Linked documents may live in SharePoint libraries; FCC owns the Knowledge metadata record.

---

# Conditional Formatting Standard

Use consistent severity colors across pages:

| Signal | Suggested behavior |
| --- | --- |
| Critical risks > 0 | Critical color. |
| High risks > 0 | Critical or warning color depending on page density. |
| Overdue commitments > 0 | Critical color. |
| Overdue dependencies > 0 | Critical color. |
| High severity dependencies > 0 | Critical color. |
| Placeholder compliance blank | Muted/neutral with placeholder label. |
| Knowledge due for review | Warning if due soon, critical if overdue. |

Do not use color to imply calculated readiness where no approved scoring formula exists.

---

# Remaining Implementation Limitations

- `Dim Owner`, `Dim Date`, `Dim Status`, and type dimensions are future derived model artifacts; MVP wireframes use base table fields.
- Knowledge-specific DAX measures are not yet created and are labeled future measure where mentioned.
- Compliance metrics remain placeholder/simple-average values until numerator and denominator fields exist.
- Program/Executive score rollups are intentionally unsupported.
- Activity source data remains outside the core report model.
