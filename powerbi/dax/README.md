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

Metric Snapshot rollup behavior is defined in `docs/METRIC_SNAPSHOT_ROLLUP_RULES.md`.

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

Metric Snapshot measures read imported historical metric rows and apply metric-specific rollup rules.

Included measures:

- `Latest Snapshot Date`
- `Open Commitments Latest`
- `Overdue Commitments Latest`
- `Open Dependencies Latest`
- `High Risks Latest`
- `Follow-Up Compliance Placeholder Latest`
- `Commitment Compliance Placeholder Latest`
- `Readiness Score Placeholder Latest`
- `Risk Score Placeholder Latest`

Count metrics sum `metric_value` across visible Initiatives at the latest snapshot date in the current filter context.

Compliance metrics use a simple average as an MVP placeholder. This should be replaced by weighted average once numerator and denominator fields are available in the snapshot feed.

Score placeholder metrics return values only at Initiative grain. Program-level and Executive-level score cards should remain blank unless an explicit higher-level MetricSnapshot is supplied by an approved scoring process.

### Initiatives

Initiative measures summarize the Initiative dimension and average imported score fields.

Included measures:

- `Active Initiatives`
- `Completed Initiatives`
- `Average Readiness Score`
- `Average Risk Score`

`readiness_score` and `risk_score` are treated as imported inputs only. No readiness or risk scoring formula is implemented in DAX.

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
- Metric Snapshot measures assume each metric has one latest date in the current filter context.
- Compliance measures are placeholder averages until weighted numerator/denominator inputs are added.
- Readiness weights are documented in the rules layer, but per-module scoring is deferred. DAX does not hardcode readiness weighting or module scoring.
- Program-level and Executive-level score snapshots require explicit approved source rows in a future snapshot design.
- No Activities measures, Activities table, or source-task reporting logic is included in the core model.
