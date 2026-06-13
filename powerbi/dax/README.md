# Power BI DAX Measures

These MVP measures support the Fundraising Command Centre Power BI semantic layer.

The measures are defined in `core_measures.dax` and assume the Sprint 2 base tables created by `powerbi/m/*.pq`:

- `Programs`
- `Initiatives`
- `Commitments`
- `Dependencies`
- `Risks`
- `Knowledge`
- `MetricSnapshots`
- `Configuration`

No Activities measures are included. Activities remain in source systems and may only feed derived FCC objects or staging processes later.

---

## Measure Groups

### Commitments

Commitment measures count FCC-owned operational obligations.

Included measures:

- `Open Commitments`
- `Completed Commitments`
- `Overdue Commitments`
- `Commitments Due Next 7 Days`
- `Commitment Completion Rate`

`Overdue Commitments` is derived from `due_date < TODAY()` and a non-completed status. It does not require an `Overdue` stored status value.

### Dependencies

Dependency measures count unresolved blockers and overdue dependencies.

Included measures:

- `Open Dependencies`
- `Resolved Dependencies`
- `Overdue Dependencies`
- `High Severity Dependencies`

`High Severity Dependencies` follows the MVP rule concept of unresolved high-severity blockers.

### Risks

Risk measures count unresolved operational risks and affected initiatives.

Included measures:

- `Open Risks`
- `High Risks`
- `Critical Risks`
- `Resolved Risks`
- `Initiatives At Risk`

`Initiatives At Risk` counts distinct Initiative references on unresolved High or Critical risks.

### Metric Snapshots

Metric Snapshot measures read imported historical metric rows.

Included measures:

- `Latest Snapshot Date`
- `Latest Metric Value`
- `Follow-Up Compliance Latest`
- `Commitment Compliance Latest`
- `Open Risks Latest`
- `Open Commitments Latest`

These measures do not calculate readiness or compliance. They return the latest imported metric value for the relevant `metric_name` in the current filter context.

### Initiatives

Initiative measures summarize the Initiative dimension and average imported score fields.

Included measures:

- `Active Initiatives`
- `Completed Initiatives`
- `Average Readiness Score`
- `Average Risk Score`

`readiness_score` and `risk_score` are treated as imported inputs only. No readiness scoring formula is implemented in DAX.

---

## Model Assumptions

- Natural ID relationships are used for the MVP.
- Program filtering should flow through `Programs -> Initiatives -> child tables`.
- Fact tables should not be directly related to `Programs`.
- Operational status applies to Commitments, Dependencies, and Risks only.
- Knowledge status remains separate and is not merged with operational status logic.
- Date logic uses table date fields directly for MVP measures; a conformed Date table can be added later.

---

## Known MVP Limitations

- Measures are written against base Sprint 2 tables, not future surrogate-key dimensions.
- `Latest Metric Value` is context-sensitive. It works best when a metric name is selected in the report context.
- Current sample snapshot data includes `high_risks_count`, but not `open_risks_count`; `Open Risks Latest` will return blank until `open_risks_count` is provided by the snapshot feed.
- Compliance measures read placeholder/config-input snapshot rows when present. They do not calculate compliance from raw activities or commitments.
- Readiness weights are documented in the rules layer, but per-module scoring is deferred. DAX does not hardcode readiness weighting or module scoring.
- No Activities measures, Activities table, or source-task reporting logic is included in the core model.
