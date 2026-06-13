# CANONICAL_SCENARIO.md

# Fundraising Command Centre (FCC)

## Canonical Synthetic Scenario — "Meridian Health Foundation"

Version: 1.0

---

# Purpose

Every FCC surface — the synthetic data generator, the Power BI
dashboards, the AI summaries, the demo, and the reference
implementation doc — must reconcile to **one** dataset with **one** set
of headline numbers. Today they do not (the reference implementation
shows 78% readiness while prototype dashboards show 76%, with different
counts elsewhere). This document fixes a single canonical scenario.

These numbers are the **acceptance criteria** for the synthetic data
generator. When the generator runs, the resulting data must produce
exactly the headline figures below when aggregated. If a dashboard or
summary shows a different number, the dashboard is wrong, not the
scenario.

This scenario adopts the figures already committed in
RE_NXT_REFERENCE_IMPLEMENTATION.md as the canonical baseline, then
specifies the full dataset shape beneath them so the headline numbers
are arithmetically reproducible.

---

# Organization Profile

| Attribute      | Value                                    |
| -------------- | ---------------------------------------- |
| Name           | Meridian Health Foundation (synthetic)   |
| Type           | Mid-sized Canadian hospital foundation   |
| CRM            | Raiser's Edge NXT                         |
| Environment    | Microsoft 365                            |
| Fiscal Year    | FY2027 (Apr 1 2026 – Mar 31 2027)        |
| Snapshot Date  | 2026-06-11 (the "as-of" date for all headline figures) |

All "today"-relative calculations (overdue, stalled, days-since) are
computed as of **2026-06-11**. The generator must anchor to this date,
not the real run date, so the numbers are stable and reproducible.

---

# Headline Figures (Executive Control Tower)

These are the canonical numbers. Every surface must reproduce them.

| Metric                          | Value  |
| ------------------------------- | ------ |
| Programs                        | 4      |
| Initiatives                     | 12     |
| Open Commitments                | 37     |
| Overdue Commitments             | 8      |
| Open Risks                      | 9      |
| Critical Risks (High severity)  | 3      |
| Open Dependencies               | 11     |
| Blocked Dependencies (High sev) | 4      |
| Follow-Up Compliance            | 84%    |
| Overall Readiness Score         | 78%    |
| Initiatives At Risk             | 3      |

---

# Programs (4)

| Program ID | Program Name           | Department             | Status |
| ---------- | ---------------------- | ---------------------- | ------ |
| PRG-0001   | Annual Giving          | Annual Giving          | Active |
| PRG-0002   | Major Gifts            | Major Gifts            | Active |
| PRG-0003   | Stewardship            | Donor Relations        | Active |
| PRG-0004   | Events                 | Events                 | Active |

---

# Initiatives (12)

Distributed across the 4 Programs. 3 of 12 are "At Risk" (readiness
below threshold OR carrying a high-severity dependency/risk).

| Initiative ID | Initiative Name              | Program  | Type          | Readiness | At Risk |
| ------------- | ---------------------------- | -------- | ------------- | --------- | ------- |
| INI-0001      | Spring Appeal                | PRG-0001 | Appeal        | 76        | No      |
| INI-0002      | Giving Tuesday               | PRG-0001 | Appeal        | 62        | Yes     |
| INI-0003      | Year-End Appeal              | PRG-0001 | Appeal        | 88        | No      |
| INI-0004      | Monthly Giving Program       | PRG-0001 | Program Cycle | 81        | No      |
| INI-0005      | Principal Gifts Portfolio    | PRG-0002 | Portfolio     | 79        | No      |
| INI-0006      | Leadership Gifts Portfolio   | PRG-0002 | Portfolio     | 71        | Yes     |
| INI-0007      | Planned Giving Portfolio     | PRG-0002 | Portfolio     | 84        | No      |
| INI-0008      | Impact Reporting Cycle       | PRG-0003 | Program Cycle | 90        | No      |
| INI-0009      | Donor Recognition Program    | PRG-0003 | Program Cycle | 83        | No      |
| INI-0010      | Foundation Reporting Program | PRG-0003 | Program Cycle | 79        | No      |
| INI-0011      | Annual Gala                  | PRG-0004 | Event         | 58        | Yes     |
| INI-0012      | Golf Tournament              | PRG-0004 | Event         | 80        | No      |

Overall Readiness Score (78%) is the Initiative-count-weighted mean of
the 12 readiness scores: (76+62+88+81+79+71+84+90+83+79+58+80)/12 =
931/12 = 77.58 → **78** (rounded). The generator must produce module
scores per Initiative that roll up to these totals once the per-module
sourcing is designed; until then, the Initiative-level Readiness Score
is seeded directly to these values.

At-Risk Initiatives (3): INI-0002, INI-0006, INI-0011.

---

# Commitments (open: 37)

37 open commitments distributed across the 12 Initiatives. Of these, 8
are overdue (Due Date < 2026-06-11 AND Status not Completed).

Status distribution (open set):

| Status      | Count |
| ----------- | ----- |
| Open        | 22    |
| In Progress | 7     |
| Overdue*    | 8     |
| **Total open** | **37** |

*Overdue is derived, not a stored status. The 8 overdue records carry a
stored Status of Open or In Progress with a past Due Date. They are
counted as Overdue in reporting.

The generator should also emit ~15 Completed commitments (not counted
in the 37 open) so Commitment Compliance and Follow-Up Compliance are
computable:

Follow-Up Compliance (84%) = Completed follow-up commitments ÷ all
follow-up commitments due on or before the snapshot date. Target the
generator so this ratio lands at 84%.

Concentration: the 8 overdue and the highest-value commitments cluster
on the 3 at-risk Initiatives (INI-0002, INI-0006, INI-0011), so the
"why is this initiative at risk" drill-down is coherent.

---

# Dependencies (open: 11)

11 open dependencies. 4 are High severity ("Blocked"). Finance is the
dominant blocking area — this is the canonical "the campaign isn't late
because of fundraising, it's waiting on Finance" story.

| Severity | Count | Notes                              |
| -------- | ----- | ---------------------------------- |
| High     | 4     | Blocked — 3 of these are Finance   |
| Medium   | 4     |                                    |
| Low      | 3     |                                    |
| **Total**| **11**|                                    |

Blocking Area distribution (open set):

| Blocking Area   | Count |
| --------------- | ----- |
| Finance         | 4     |
| Data            | 3     |
| Marketing       | 2     |
| IT              | 1     |
| Legal           | 1     |

The 4 High-severity dependencies impact the 3 at-risk Initiatives plus
one more, driving the "blocked" narrative on the Dependencies & Risks
page.

---

# Risks (open: 9)

9 open risks. 3 are High severity (Critical). Risks are a mix of
manually entered and rule-generated.

| Severity | Count |
| -------- | ----- |
| High     | 3     |
| Medium   | 4     |
| Low      | 2     |
| **Total**| **9** |

Risk Type distribution (open set):

| Risk Type    | Count | Source |
| ------------ | ----- | ------ |
| Pipeline     | 2     | Rule (stalled prospect) |
| Follow-Up    | 2     | Rule (missing next action) |
| Commitment   | 1     | Rule (overdue proposal) |
| Readiness    | 1     | Rule (readiness threshold breach) |
| Dependency   | 1     | Rule (overdue high-sev dependency) |
| Operational  | 1     | Manual |
| Data Quality | 1     | Rule |

The 3 Critical (High) risks map to the 3 at-risk Initiatives, closing
the loop: an at-risk Initiative has an identifiable critical risk
and/or a blocking dependency behind it.

---

# Cross-Surface Reconciliation Rules

For the dataset to be coherent, these invariants must hold. They are
generator test assertions:

1. **Readiness mean.** Mean of the 12 Initiative readiness scores =
   78 (rounded). ✔ verified above (77.58 → 78).

2. **At-risk coherence.** Every "At Risk" Initiative (3) has at least
   one High-severity dependency OR one High-severity risk. No Initiative
   is flagged at risk without a traceable cause.

3. **Critical risk count.** Exactly 3 risks are High severity, and they
   sit on the 3 at-risk Initiatives.

4. **Finance dominance.** Finance is the single largest Blocking Area
   (4 of 11), so the AI bottleneck summary naming Finance is data-true.

5. **Overdue arithmetic.** Exactly 8 open commitments have Due Date <
   2026-06-11 and Status ≠ Completed.

6. **Compliance ratios land on target.** Follow-Up Compliance computes
   to 84% (±0 after rounding) from the generated completed/total
   follow-up commitments.

7. **Initiative-only linking.** Every Commitment, Dependency, and Risk
   references a valid Initiative ID; Program is never stored on them and
   is always resolvable via the Initiative.

8. **Referential integrity.** Every Initiative references a valid
   Program ID; every Owner referenced exists in the owner set; no
   orphan foreign keys.

---

# What The Generator Must Emit

Per FIELD_REGISTRY.md field definitions, anchored to snapshot date
2026-06-11:

| File                  | Rows (approx)                     |
| --------------------- | --------------------------------- |
| programs.csv          | 4                                 |
| initiatives.csv       | 12                                |
| commitments.csv       | ~52 (37 open + ~15 completed)     |
| dependencies.csv      | ~15 (11 open + ~4 resolved)       |
| risks.csv             | ~13 (9 open + ~4 resolved)        |
| knowledge.csv         | ~20 (mixed status)                |
| metric_snapshots.csv  | ~30 (multiple metrics × dates)    |
| configuration.csv     | seed rows incl. readiness weights |

Metric Snapshots should include at least two snapshot dates (e.g.
2026-06-04 and 2026-06-11) so trend/"vs last week" deltas on the
dashboards are computable, with the 2026-06-11 snapshot matching the
headline figures above.

---

# Note On The 76% vs 78% Discrepancy

The prototype dashboards built earlier used 76% readiness; the
reference implementation and this canonical scenario use **78%**. The
canonical value is **78%**. Any prototype, mockup, or demo asset still
showing 76% should be updated to 78% before a live demo so every
surface reconciles. This is a values fix, not a schema fix.
