# Metric Snapshot Rollup Rules

# Fundraising Command Centre (FCC)

Version: 1.0

---

# Purpose

This document defines how `MetricSnapshots` roll up from Initiative-level records to Program and Executive views before Power BI report page specifications are built.

Metric Snapshots are first-class facts in the FCC semantic model. They store management metrics that have already been produced by the Rules Layer, configuration, or approved source inputs. Power BI should aggregate these records according to the metric type; it should not infer scoring formulas from unrelated operational records.

---

# Core Principles

- Select the latest `snapshot_date` within the current report filter context.
- Apply metric-specific rollup behavior after selecting the latest snapshot date.
- Do not use `MAX(metric_value)` as a generic portfolio-level card measure.
- Do not invent readiness or risk scoring formulas in Power BI.
- Do not derive activity-based compliance directly from Activities in the core model.
- Program and Executive levels should flow through the Initiative relationship path, unless a metric is explicitly provided as a Program-level or organization-level snapshot in the future.

---

# Required Metric Names

The MVP snapshot feed should use these metric names exactly:

| Metric name | Type | MVP rollup behavior |
| --- | --- | --- |
| `open_commitments_count` | Count | Sum across Initiatives |
| `overdue_commitments_count` | Count | Sum across Initiatives |
| `open_dependencies_count` | Count | Sum across Initiatives |
| `high_risks_count` | Count | Sum across Initiatives |
| `follow_up_compliance` | Percentage/compliance | Weighted average when numerator/denominator are available; simple average as MVP placeholder |
| `commitment_compliance` | Percentage/compliance | Weighted average when numerator/denominator are available; simple average as MVP placeholder |
| `readiness_score_placeholder` | Score placeholder | Initiative-level imported value only; no Program rollup formula |
| `risk_score_placeholder` | Score placeholder | Initiative-level imported value only; no Program rollup formula |

---

# Count Metrics

Examples:

- `open_commitments_count`
- `overdue_commitments_count`
- `open_dependencies_count`
- `high_risks_count`

Expected rollup:

- Sum `metric_value` across Initiatives at the latest snapshot date in the current filter context.
- Program-level cards should sum the latest Initiative snapshot rows belonging to that Program.
- Executive-level cards should sum the latest Initiative snapshot rows visible in the report context.

Count metrics are additive because each Initiative snapshot represents a distinct operational portfolio slice.

---

# Percentage And Compliance Metrics

Examples:

- `follow_up_compliance`
- `commitment_compliance`

Expected final rollup:

- Use weighted average when numerator and denominator fields are available.
- Example: total completed follow-ups divided by total required follow-ups due.
- Example: total completed commitments divided by total commitments in scope.

MVP placeholder behavior:

- Use simple average of imported `metric_value` rows at the latest snapshot date.
- This is only a placeholder because the current `MetricSnapshots` structure does not include numerator and denominator columns.
- Report specs must label these as placeholder/config-input metrics until weighted rollup inputs exist.

Do not calculate follow-up compliance from Activities in the core model. Activities remain in source systems or staging.

---

# Score Metrics

Examples:

- `readiness_score_placeholder`
- `risk_score_placeholder`

Expected rollup:

- Do not invent a readiness or risk scoring formula.
- Use only imported Initiative-level score values.
- Program-level score should be blank unless a Program-level MetricSnapshot is explicitly supplied as its own approved source metric.
- Executive-level score should be blank unless an Executive-level MetricSnapshot is explicitly supplied as its own approved source metric.

The Rules Layer documents readiness weights, but per-module scoring remains deferred. Power BI must not hardcode module scoring or infer score rollups from counts, risks, dependencies, or commitments.

---

# Latest Value Behavior

Latest snapshot selection must happen within the current filter context.

For a Program page, the latest snapshot date is the latest date among the Initiative snapshots visible for that Program and metric name. For an Executive page, it is the latest date among all visible Initiative snapshots and the selected metric name.

After selecting the latest date:

- Count metrics use `SUM(metric_value)`.
- Percentage/compliance metrics use a simple average for MVP, later replaced by weighted average.
- Score placeholder metrics return a value only at Initiative grain unless an explicit higher-level snapshot exists.

Do not use `MAX(metric_value)` blindly for portfolio-level cards. `MAX(metric_value)` can return the largest child Initiative value rather than the portfolio value.

---

# Future Enhancements

Future snapshot design may add:

- metric grain, such as Initiative, Program, Executive, or Organization
- numerator and denominator columns for weighted compliance
- approved Program-level and Executive-level score snapshots
- metric metadata describing rollup behavior

Until those fields exist, DAX measures should keep rollup logic explicit and conservative.
