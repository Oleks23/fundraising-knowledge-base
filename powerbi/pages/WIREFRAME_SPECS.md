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
- Score placeholder visuals must use `Initiatives[initiative_id]` in filter/drill context; display `Initiatives[initiative_name]` as the readable label.
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
| Open Commitments | `Open Commitments Latest` | Red if > 0; green if = 0. |
| Overdue Commitments | `Overdue Commitments Latest` | Red if > 0; green if = 0. |
| Open Dependencies | `Open Dependencies Latest` | Red if > 0; green if = 0. |
| High Risks | `High Risks Latest` | Red if > 0; green if = 0. |
| Critical Risks | `Critical Risks` | Red if > 0; green if = 0. |
| Initiatives At Risk | `Initiatives At Risk` | Red if > 0; green if = 0. |
| Follow-Up Compliance Placeholder | `Follow-Up Compliance Placeholder Latest` | Label as placeholder/config input. Use muted styling if blank. |
| Commitment Compliance Placeholder | `Commitment Compliance Placeholder Latest` | Label as placeholder/config input. Use muted styling if blank. |

Threshold-based formatting is future/config-driven and should not be implemented in MVP unless configuration-driven thresholds are added.

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Program Operational Load | Clustered bar | Axis: `Programs[program_name]`; Values: `Open Commitments Latest`, `Overdue Commitments Latest`, `Open Dependencies Latest`, `High Risks Latest` | Sort by combined operational burden descending. |
| Initiatives Requiring Intervention | Ranked bar or matrix | `Initiatives[initiative_name]`; Values: `Overdue Commitments`, `High Risks`, `High Severity Dependencies` | Red for nonzero risk/blocker/overdue values; green when all are 0. |
| Risk Severity Mix | Stacked bar or donut | Legend: `Risks[severity]`; Values: count of `Risks[risk_id]`; visual filter `Risks[status] <> "Resolved"` | Red for Critical/High categories. |
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
- `Initiatives[initiative_name]` -> Initiative Detail, with `Initiatives[initiative_id]` included in drill context.
- `Risks[risk_id]` -> Risk Detail.
- `Commitments[commitment_id]` -> Commitment Detail.

## Warnings/Limitations

- Do not show Executive readiness/risk score cards in MVP.
- Compliance cards are placeholders until numerator/denominator fields exist.
- `Programs[executive_owner]` is Program-specific and does not filter all child object owners.
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
| Initiative | `Initiatives[initiative_id]` | Use `Initiatives[initiative_name]` as readable label where available. |
| Initiative Status | `Initiatives[status]` | Initiative lifecycle only. |
| Initiative Type | `Initiatives[initiative_type]` | Initiative categorization. |
| Initiative Owner | `Initiatives[owner]` | Object-specific owner slicer. |
| Department | `Initiatives[department]` | Initiative-level department view. |
| Target Date | `Initiatives[target_date]` | Use date range or relative slicer. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Active Initiatives | `Active Initiatives` | Neutral. |
| Completed Initiatives | `Completed Initiatives` | Green when > 0; neutral when 0. |
| Initiatives At Risk | `Initiatives At Risk` | Red if > 0; green if = 0. |
| Open Commitments | `Open Commitments` | Red if > 0; green if = 0. |
| Open Dependencies | `Open Dependencies` | Red if > 0; green if = 0. |
| Open Risks | `Open Risks` | Red if > 0; green if = 0. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Initiative Portfolio Matrix | Matrix | Rows: `Programs[program_name]`, `Initiatives[initiative_name]`; include `Initiatives[initiative_id]` in detail/drill context; Values: `Initiatives[owner]`, `Initiatives[status]`, `Initiatives[target_date]`, `Open Commitments`, `Open Dependencies`, `High Risks` | Primary portfolio scan. |
| Initiative Status by Program | Stacked bar | Axis: `Programs[program_name]`; Legend: `Initiatives[status]`; Values: count of `Initiatives[initiative_id]` | Show portfolio lifecycle distribution. |
| Initiative Owner Workload | Bar chart | Axis: `Initiatives[owner]`; Values: `Active Initiatives` | MVP object-specific owner view. |
| Target Date Timeline | Bar by month | Axis: month from `Initiatives[target_date]`; Values: count of `Initiatives[initiative_id]` | Yellow for due within 7 days; red for past target date; green for no near-term/past-due target in context. |

## Future Visuals — Do Not Build in MVP

| Future visual | Future model requirement | Notes |
| --- | --- | --- |
| Future Conformed Owner Workload | Future `Dim Owner` table | Would use future `Dim Owner` plus Active Initiatives, Open Commitments, Open Dependencies, and Open Risks. Do not build in MVP. |

## Tables

| Table | Fields |
| --- | --- |
| Initiative Register | `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Programs[program_name]`, `Initiatives[initiative_type]`, `Initiatives[owner]`, `Initiatives[department]`, `Initiatives[status]`, `Initiatives[start_date]`, `Initiatives[target_date]`, `Initiatives[goal_amount]`, `Initiatives[source_system]`, `Initiatives[source_record_id]` |
| Portfolio Risk/Execution Summary | `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Open Commitments`, `Overdue Commitments`, `Open Dependencies`, `High Risks`, `Critical Risks`, `High Severity Dependencies` |

## Drillthrough Targets

- `Programs[program_name]` -> Program Detail.
- `Initiatives[initiative_name]` -> Initiative Detail, with `Initiatives[initiative_id]` included in drill context.

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
| Slicer rail | Left vertical rail | Program, Initiative ID, Initiative readable label, Initiative Owner, Initiative Status, Snapshot Date, Threshold Status. |
| KPI strip | Top body | Initiative-level score placeholders plus latest count metrics. |
| Main visual area | Middle body | Execution Pressure Trend, Due Window, Dependency and Risk visuals. |
| Detail table area | Bottom body | Metric snapshots, execution commitments, blocking dependencies, readiness risks. |
| Notes | Bottom right | Score placeholder warning. |

## Slicers

| Slicer | Field | Notes |
| --- | --- | --- |
| Program | `Programs[program_name]` | Shared Program filter. |
| Initiative ID | `Initiatives[initiative_id]` | Required for `Readiness Score Placeholder Latest` and `Risk Score Placeholder Latest` context. |
| Initiative Label | `Initiatives[initiative_name]` | Display/readable label only; keep `Initiatives[initiative_id]` in filter/drill context. |
| Initiative Owner | `Initiatives[owner]` | Object-specific owner slicer. |
| Initiative Status | `Initiatives[status]` | Initiative lifecycle only. |
| Snapshot Date | `MetricSnapshots[snapshot_date]` | Snapshot filter. |
| Threshold Status | `MetricSnapshots[threshold_status]` | Snapshot threshold view. |

## KPI Cards

| Card | Measure | Conditional formatting |
| --- | --- | --- |
| Readiness Score Placeholder | `Readiness Score Placeholder Latest` | Show only when `Initiatives[initiative_id]` is in context; muted/blank otherwise. Do not color as calculated readiness. |
| Risk Score Placeholder | `Risk Score Placeholder Latest` | Show only when `Initiatives[initiative_id]` is in context; muted/blank otherwise. Do not color as calculated risk score. |
| Open Commitments | `Open Commitments Latest` | Red if > 0; green if = 0. |
| Overdue Commitments | `Overdue Commitments Latest` | Red if > 0; green if = 0. |
| Open Dependencies | `Open Dependencies Latest` | Red if > 0; green if = 0. |
| High Risks | `High Risks Latest` | Red if > 0; green if = 0. |
| Due Next 7 Days | `Commitments Due Next 7 Days` | Yellow if > 0; green if = 0. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Initiative Readiness Snapshot | KPI/card group | `Initiatives[initiative_id]` in context; display `Initiatives[initiative_name]`; `Readiness Score Placeholder Latest`, `Risk Score Placeholder Latest`, `Open Commitments Latest`, `Overdue Commitments Latest`, `Open Dependencies Latest`, `High Risks Latest` | Keep scores Initiative-only. |
| Execution Pressure Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Legend: `MetricSnapshots[metric_name]`; Value: `MetricSnapshots[metric_value]`; filter to count metrics | Do not trend score placeholders as Program rollups. |
| Commitments by Due Window | Bar chart | Buckets from `Commitments[due_date]`; Values: count of `Commitments[commitment_id]` | Red for overdue, yellow for 0-7 days, green for no due/overdue items. |
| Dependencies Blocking Execution | Bar/table | `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[severity]`, `Dependencies[due_date]` | Red if high severity or overdue; yellow if due within 7 days. |
| Risks by Type and Severity | Stacked bar | Axis: `Risks[risk_type]`; Legend: `Risks[severity]`; Values: count of `Risks[risk_id]` | Filter out resolved risks for active risk view. Red for High/Critical > 0. |

## Tables

| Table | Fields |
| --- | --- |
| Readiness Metric Snapshots | `MetricSnapshots[snapshot_date]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `MetricSnapshots[metric_name]`, `MetricSnapshots[metric_value]`, `MetricSnapshots[metric_unit]`, `MetricSnapshots[threshold_status]`, `MetricSnapshots[source_system]`, `MetricSnapshots[notes]` |
| Execution Commitments | `Commitments[commitment_id]`, `Commitments[commitment_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |
| Blocking Dependencies | `Dependencies[dependency_id]`, `Dependencies[dependency_name]`, `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[status]`, `Dependencies[severity]`, `Dependencies[impact_description]` |
| Readiness Risks | `Risks[risk_id]`, `Risks[risk_name]`, `Risks[risk_type]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[owner]`, `Risks[status]`, `Risks[mitigation_plan]`, `Risks[target_resolution_date]` |

## Drillthrough Targets

- `Initiatives[initiative_name]` -> Initiative Detail, with `Initiatives[initiative_id]` included in drill context.
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
| Initiative | `Initiatives[initiative_id]` | Use `Initiatives[initiative_name]` as readable label where available. |
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
| Open Dependencies | `Open Dependencies` | Red if > 0; green if = 0. |
| Overdue Dependencies | `Overdue Dependencies` | Red if > 0; green if = 0. |
| High Severity Dependencies | `High Severity Dependencies` | Red if > 0; green if = 0. |
| Open Risks | `Open Risks` | Red if > 0; green if = 0. |
| High Risks | `High Risks` | Red if > 0; green if = 0. |
| Critical Risks | `Critical Risks` | Red if > 0; green if = 0. |
| Initiatives At Risk | `Initiatives At Risk` | Red if > 0; green if = 0. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Dependency Blocker Map | Matrix | Rows: `Dependencies[blocking_area]`; Columns: `Dependencies[impacted_area]`; Values: `Open Dependencies`, `High Severity Dependencies` | Red for high severity/open blockers > 0. |
| Risk Severity by Program | Stacked bar | Axis: `Programs[program_name]`; Legend: `Risks[severity]`; Values: count of `Risks[risk_id]` | Filter out resolved risks for active view. Red for High/Critical > 0. |
| Risk Type Mix | Bar or treemap | `Risks[risk_type]`; Values: count of `Risks[risk_id]` | Red for High/Critical tooltip values > 0. |
| Dependency Due Timeline | Bar by due bucket | Buckets from `Dependencies[due_date]`; Values: `Open Dependencies` | Red for overdue, yellow for due within 7 days, green for count = 0. |
| Risk Resolution Timeline | Bar by date | Axis: `Risks[target_resolution_date]`; Values: `Open Risks` | Yellow for due within 7 days; red for past target date. |

## Tables

| Table | Fields |
| --- | --- |
| Dependency Register | `Dependencies[dependency_id]`, `Dependencies[dependency_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Dependencies[dependency_type]`, `Dependencies[blocking_area]`, `Dependencies[impacted_area]`, `Dependencies[owner]`, `Dependencies[due_date]`, `Dependencies[status]`, `Dependencies[severity]`, `Dependencies[impact_description]`, `Dependencies[resolution_notes]` |
| Risk Register | `Risks[risk_id]`, `Risks[risk_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Risks[risk_type]`, `Risks[severity]`, `Risks[likelihood]`, `Risks[status]`, `Risks[owner]`, `Risks[date_identified]`, `Risks[target_resolution_date]`, `Risks[mitigation_plan]`, `Risks[source_system]`, `Risks[source_record_id]` |
| At-Risk Initiatives | `Programs[program_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Initiatives[owner]`, `Initiatives[status]`, `High Severity Dependencies`, `High Risks`, `Critical Risks` |

## Drillthrough Targets

- `Dependencies[dependency_id]` -> Dependency Detail.
- `Risks[risk_id]` -> Risk Detail.
- `Initiatives[initiative_name]` -> Initiative Detail, with `Initiatives[initiative_id]` included in drill context.
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
| Initiative | `Initiatives[initiative_id]` | Use `Initiatives[initiative_name]` as readable label where available. |
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
| Open Commitments | `Open Commitments` | Red if > 0; green if = 0. |
| Completed Commitments | `Completed Commitments` | Green when > 0; neutral when 0. |
| Overdue Commitments | `Overdue Commitments` | Red if > 0; green if = 0. |
| Due Next 7 Days | `Commitments Due Next 7 Days` | Yellow if > 0; green if = 0. |
| Commitment Completion Rate | `Commitment Completion Rate` | Use percentage format; no target color unless future/config-driven threshold exists. |
| Follow-Up Compliance Placeholder | `Follow-Up Compliance Placeholder Latest` | Label placeholder/config input. |
| Commitment Compliance Placeholder | `Commitment Compliance Placeholder Latest` | Label placeholder/config input. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Commitments by Status | Stacked bar | Axis/legend: `Commitments[status]`; Values: count of `Commitments[commitment_id]` | Do not merge with Knowledge status. |
| Overdue by Commitment Owner | Bar chart | Axis: `Commitments[owner]`; Values: `Overdue Commitments` | Commitment-owner only. Red if overdue count > 0. |
| Due Date Calendar / Timeline | Calendar or weekly bar | Axis: `Commitments[due_date]`; Values: count of `Commitments[commitment_id]` | Red for overdue, yellow for due within 7 days, green for count = 0. |
| Commitment Type Mix | Bar chart | Axis: `Commitments[commitment_type]`; Values: count of `Commitments[commitment_id]` | Show obligation categories. |
| Compliance Placeholder Trend | Line chart | Axis: `MetricSnapshots[snapshot_date]`; Values: `MetricSnapshots[metric_value]`; filter `MetricSnapshots[metric_name]` to `follow_up_compliance`, `commitment_compliance` | Placeholder only; no Activities calculation. |

## Tables

| Table | Fields |
| --- | --- |
| Commitment Work Queue | `Commitments[commitment_id]`, `Commitments[commitment_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Commitments[commitment_type]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[status]`, `Commitments[priority]`, `Commitments[value_amount]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]`, `Commitments[notes]` |
| Overdue Commitments | `Commitments[commitment_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Commitments[owner]`, `Commitments[due_date]`, `Commitments[priority]`, `Commitments[escalation_level]`, `Commitments[source_system]`, `Commitments[source_record_id]` |
| Source Traceability | `Commitments[commitment_id]`, `Commitments[source_system]`, `Commitments[source_record_id]`, `Commitments[notes]` |

## Drillthrough Targets

- `Commitments[commitment_id]` -> Commitment Detail.
- `Initiatives[initiative_name]` -> Initiative Detail, with `Initiatives[initiative_id]` included in drill context.

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
| Initiative | `Initiatives[initiative_id]` | Optional; show `Initiatives[initiative_name]` as readable label. Some Knowledge may be organization-wide. |
| Knowledge Type | `Knowledge[knowledge_type]` | Knowledge-specific. |
| Knowledge Status | `Knowledge[status]` | Separate from operational status. |
| Source Authority | `Knowledge[source_authority]` | Knowledge governance field. |
| Knowledge Owner | `Knowledge[owner]` | Knowledge-specific owner slicer. |
| Review Date | `Knowledge[review_date]` | Date table recommended later. |
| Tags | `Knowledge[tags]` | Text/tag filter. |

## KPI Cards

| Card | Measure / field | Conditional formatting |
| --- | --- | --- |
| Knowledge Assets | Count of `Knowledge[knowledge_id]` | Existing implicit count; neutral. |
| Approved Assets | Count of `Knowledge[knowledge_id]` filtered to `Knowledge[status] = "Approved"` | Existing implicit count; green when > 0. |
| Draft Assets | Count of `Knowledge[knowledge_id]` filtered to `Knowledge[status] = "Draft"` | Existing implicit count; yellow if > 0. |
| Assets Due For Review | Future measure | Future measure; for MVP visual-level count, red if overdue count > 0. |
| Assets Missing Owner | Future measure | Future measure; for MVP visual-level count, red if blank owner count > 0. |

## Charts

| Chart | Type | Fields / measures | Notes |
| --- | --- | --- | --- |
| Knowledge by Program and Initiative | Matrix | Rows: `Programs[program_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`; Columns: `Knowledge[knowledge_type]`; Values: count of `Knowledge[knowledge_id]` | Do not force blank Initiative Knowledge into artificial Initiative. |
| Knowledge Status Mix | Bar or donut | `Knowledge[status]`; Values: count of `Knowledge[knowledge_id]` | Keep separate from operational status. |
| Review Calendar | Timeline/table | `Knowledge[review_date]`, `Knowledge[title]`, `Knowledge[owner]` | Red for overdue review dates, yellow for due within 7 days. |
| Source Authority Mix | Bar chart | `Knowledge[source_authority]`; Values: count of `Knowledge[knowledge_id]` | Shows Working/Approved/Official. |
| Tag Explorer | Table/slicer | `Knowledge[tags]`, `Knowledge[title]`, `Knowledge[knowledge_type]` | Supports navigation. |

## Tables

| Table | Fields |
| --- | --- |
| Knowledge Asset Register | `Knowledge[knowledge_id]`, `Knowledge[title]`, `Knowledge[knowledge_type]`, `Programs[program_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, `Knowledge[owner]`, `Knowledge[status]`, `Knowledge[source_authority]`, `Knowledge[review_date]`, `Knowledge[document_link]`, `Knowledge[tags]` |
| Assets Due For Review | `Knowledge[title]`, `Knowledge[knowledge_type]`, `Knowledge[owner]`, `Knowledge[status]`, `Knowledge[source_authority]`, `Knowledge[review_date]`, `Programs[program_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]` |
| Initiative Knowledge Coverage | `Programs[program_name]`, `Initiatives[initiative_id]`, `Initiatives[initiative_name]`, count of `Knowledge[knowledge_id]`, count filtered to `Knowledge[status] = "Approved"`, minimum future `Knowledge[review_date]` |

## Drillthrough Targets

- `Knowledge[knowledge_id]` -> Knowledge Detail.
- `Initiatives[initiative_name]` -> Initiative Detail, with `Initiatives[initiative_id]` included in drill context.
- `Programs[program_name]` -> Program Detail.
- `Knowledge[document_link]` -> SharePoint/knowledge document target when available.

## Warnings/Limitations

- Current DAX has no Knowledge-specific explicit measures; use implicit counts or future measures as labeled.
- `Knowledge[status]` is not operational status.
- `Knowledge[owner]` filters Knowledge visuals only.
- Linked documents may live in SharePoint libraries; FCC owns the Knowledge metadata record.

---

# Conditional Formatting Standard

Use simple MVP-safe color rules across pages:

| Signal | MVP behavior |
| --- | --- |
| Critical risks count | Red if count > 0; green if count = 0. |
| High risks count | Red if count > 0; green if count = 0. |
| Overdue commitments count | Red if count > 0; green if count = 0. |
| Overdue dependencies count | Red if count > 0; green if count = 0. |
| High severity dependencies count | Red if count > 0; green if count = 0. |
| Due within 7 days | Yellow if count > 0; green if count = 0. |
| Placeholder compliance blank | Muted/neutral with placeholder label. |
| Knowledge due for review | Yellow if due within 7 days; red if overdue; green if no due/overdue items. |

Threshold-based formatting is future/config-driven and should only be implemented after configuration-backed thresholds are available.

Do not use color to imply calculated readiness where no approved scoring formula exists.

---

# Remaining Implementation Limitations

- `Dim Owner`, `Dim Date`, `Dim Status`, and type dimensions are future derived model artifacts; MVP wireframes use base table fields.
- Knowledge-specific DAX measures are not yet created and are labeled future measure where mentioned.
- Compliance metrics remain placeholder/simple-average values until numerator and denominator fields exist.
- Program/Executive score rollups are intentionally unsupported.
- Activity source data remains outside the core report model.
