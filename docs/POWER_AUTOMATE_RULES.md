# POWER_AUTOMATE_RULES.md

# Fundraising Command Centre (FCC)

## Rules & Automation Framework

Version: 1.0

---

# Purpose

This document defines the operational rules used by the Fundraising Command Centre (FCC).

Rules transform source-system data into operational intelligence.

The Rules Layer is the operational brain of FCC.

Rules create:

* Risks
* Alerts
* Readiness Scores
* Compliance Metrics
* Escalations
* Management Notifications

---

# Design Principles

## Principle 1

Rules generate operational intelligence.

Rules do not modify source-system records.

---

## Principle 2

CRM remains the source of donor truth.

Planner remains the source of task truth.

FCC consumes data and generates insights.

---

## Principle 3

All rules must be explainable.

Leadership should understand:

* why a risk exists
* why a score changed
* why an alert was generated

---

## Principle 4

Thresholds should be configurable.

Thresholds belong in:

Configuration List

Examples:

* Follow-Up SLA
* Readiness Threshold
* Risk Escalation Threshold

---

# Rule Categories

FCC Rules are grouped into:

1. Commitment Rules
2. Dependency Rules
3. Risk Rules
4. Readiness Rules
5. Compliance Rules
6. Alert Rules
7. Snapshot Rules
8. Knowledge Rules

---

# Commitment Rules

Purpose:

Monitor operational obligations.

---

## Commitment Overdue

Rule:

```text
Due Date < Today
AND
Status <> Complete
```

Action:

Create Alert

Severity:

Medium

---

## Commitment Critical

Rule:

```text
Due Date < Today - 14 Days
AND
Status <> Complete
```

Action:

Create Risk

Type:

Commitment Risk

Severity:

High

---

## Commitment Due Soon

Rule:

```text
Due Date <= Today + 7 Days
AND
Status <> Complete
```

Action:

Create Alert

Severity:

Low

---

# Dependency Rules

Purpose:

Monitor blockers.

---

## Dependency Overdue

Rule:

```text
Dependency Due Date < Today
AND
Status <> Resolved
```

Action:

Create Risk

Type:

Dependency Risk

---

## Critical Dependency

Rule:

```text
Severity = High
AND
Status <> Resolved
```

Action:

Escalation Alert

---

## Initiative Blocked

Rule:

```text
High Severity Dependency Exists
```

Action:

Flag Initiative

Status:

At Risk

---

# Risk Rules

Purpose:

Identify operational threats.

---

## Stalled Prospect

Typical Source:

RE NXT

Rule:

```text
No Completed Activity
within 90 Days
```

Action:

Create Risk

Type:

Pipeline Risk

---

## Missing Next Action

Typical Source:

RE NXT

Rule:

```text
Active Opportunity
AND
No Future Activity
```

Action:

Create Risk

Type:

Follow-Up Risk

---

## High Value Inactivity

Rule:

```text
Opportunity Value > Threshold
AND
No Activity within SLA
```

Action:

Create Risk

Severity:

High

---

# Readiness Rules

Purpose:

Measure Initiative readiness.

---

## Readiness Inputs

Readiness is scored across five modules (see Readiness Score below):

* Prospect Coverage
* Case for Support
* Finance Setup
* Marketing Assets
* Stewardship Plan

The operational signals that feed each module's score (open and
overdue commitments, blocking dependencies, critical risks, milestone
completion) are inputs to the per-module scores. How they roll up into
each module score is an open question (see "Open implementation
question" below).

---

## Readiness Score

Scale:

0 – 100

Readiness is **module-weighted**. An Initiative's readiness is the
weighted sum of its per-module scores, using these canonical weights:

| Module            | Weight |
| ----------------- | ------ |
| Prospect Coverage | 40%    |
| Case for Support  | 20%    |
| Finance Setup     | 15%    |
| Marketing Assets  | 15%    |
| Stewardship Plan  | 10%    |

These weights are the single source of truth for readiness and are
stored in the Configuration List (Config Area = "Readiness Weights"),
so they can be tuned per client without code changes. The Power BI
DAX measure and any synthetic data must use these same weights.

Stored In:

Metric Snapshots

### Open implementation question — per-module scoring

How each Initiative's individual module scores (e.g. its Prospect
Coverage %) are produced is **deferred and not yet designed**. The
weights are fixed; the inputs that roll up into each module score are
not. This will be resolved during scenario validation. Until then:

* Do not invent a "Readiness Category" field on Commitments,
  Dependencies, or other records to make the math work.
* Treat per-module scores as an input to be supplied (manually,
  via a readiness checklist, or by a future rule), not as a
  derivation that already exists in the model.

Codex and implementers must not hardcode a module-scoring formula
ahead of this decision.

---

## Readiness Threshold Breach

Rule:

```text
Readiness Score < Configured Threshold
```

Action:

Create Risk

Type:

Readiness Risk

---

# Compliance Rules

Purpose:

Measure execution discipline.

---

## Follow-Up Compliance

Example:

```text
Required Follow-Ups Completed
÷
Required Follow-Ups Due
```

Output:

Compliance Percentage

Stored In:

Metric Snapshot

---

## Commitment Compliance

Example:

```text
Completed Commitments
÷
Total Commitments
```

Output:

Compliance Percentage

---

## Stewardship Compliance

Example:

```text
Completed Reports
÷
Required Reports
```

Output:

Compliance Percentage

---

# Alert Rules

Purpose:

Generate management notifications.

---

## New High Risk

Rule:

```text
Risk Severity = High
```

Action:

Create Alert

Notify:

Owner

Manager

---

## Multiple Open Risks

Rule:

```text
Open Risks > Threshold
```

Action:

Escalation Alert

---

## Readiness Decline

Rule:

```text
Readiness Score decreases
more than configured percentage
```

Action:

Create Alert

---

# Snapshot Rules

Purpose:

Create historical metrics.

---

## Weekly Snapshot

Frequency:

Weekly

Captures:

* Readiness Score
* Risk Count
* Commitment Count
* Dependency Count
* Compliance Metrics

Stores:

Metric Snapshot Record

---

## Monthly Snapshot

Frequency:

Monthly

Captures:

Trend Metrics

Stores:

Metric Snapshot Record

---

# Knowledge Rules

Purpose:

Maintain institutional knowledge.

---

## Review Due

Rule:

```text
Review Date < Today
```

Action:

Create Alert

---

## Missing Owner

Rule:

```text
Knowledge Asset Owner is Blank
```

Action:

Create Risk

Type:

Governance Risk

---

# Escalation Framework

## Level 1

Owner Notification

---

## Level 2

Manager Notification

Triggered After:

Configured Delay

---

## Level 3

Director Notification

Triggered After:

Configured Delay

---

# Power Automate Flows

MVP Flow Set

---

## Flow 1

Import RE NXT Data

Purpose:

Load CRM export files.

---

## Flow 2

Import Planning Data

Purpose:

Load Planner / Asana / Smartsheet exports.

---

## Flow 3

Commitment Monitoring

Purpose:

Generate commitment alerts.

---

## Flow 4

Dependency Monitoring

Purpose:

Generate dependency alerts.

---

## Flow 5

Risk Generation

Purpose:

Create operational risks.

---

## Flow 6

Readiness Calculation

Purpose:

Calculate Initiative readiness.

---

## Flow 7

Snapshot Creation

Purpose:

Create weekly and monthly snapshots.

---

## Flow 8

Teams Notification

Purpose:

Send alerts and summaries.

---

# AI Integration

AI should consume:

* Metric Snapshots
* Risks
* Commitments
* Dependencies

AI should not calculate metrics.

AI explains what has already been calculated.

Outputs:

* Weekly Digest
* Executive Briefing
* Readiness Summary
* Risk Summary

---

# Future Rules

Potential future enhancements:

* Predictive Risk Scoring
* Forecast Variance Detection
* Workload Balancing
* Capacity Analysis
* Fundraiser Prioritization
* AI Recommendations

These are outside MVP scope.

---

# Success Criteria

The Rules Layer succeeds when FCC can automatically identify:

* What is overdue
* What is blocked
* What is at risk
* What requires intervention

without requiring manual review of source systems.
