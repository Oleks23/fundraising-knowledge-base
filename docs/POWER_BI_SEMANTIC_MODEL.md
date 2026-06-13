# POWER_BI_SEMANTIC_MODEL.md

# Fundraising Command Centre (FCC)

## Power BI Semantic Model

Version: 1.0

---

# Purpose

This document defines the Power BI semantic model for the Fundraising Command Centre.

The model is designed to support:

* Executive decision-making
* Operational management
* Readiness monitoring
* Risk management
* Commitment accountability
* AI-generated summaries

The model is built from FCC operational objects rather than directly from CRM tables.

---

# Design Principles

## Principle 1

Model management questions.

Not source systems.

Example:

Bad:

* Campaign Table
* Opportunity Table
* Action Table

Good:

* Commitments
* Risks
* Dependencies
* Readiness
* Compliance

---

## Principle 2

Use a star schema whenever possible.

---

## Principle 3

Metric Snapshots are first-class facts.

Historical snapshots are more valuable than current-state records.

---

## Principle 4

Power BI is the primary Command Centre interface.

Reports should support management decisions.

Not database exploration.

---

# Semantic Model Overview

```text
Dimensions

Dim Program
Dim Initiative
Dim Owner
Dim Department
Dim Date
Dim Commitment Type
Dim Risk Type
Dim Dependency Type
Dim Status

       ↓

Facts

Fact Commitments
Fact Dependencies
Fact Risks
Fact Metric Snapshots
```

---

# Core Dimensions

## Dim Program

Examples:

* Annual Giving
* Major Gifts
* Stewardship
* Events
* Corporate Partnerships

Key Fields:

* Program Key
* Program Name
* Program Type
* Department
* Executive Owner

---

## Dim Initiative

Examples:

* Spring Appeal
* Principal Gifts Portfolio
* Annual Gala
* Donor Reporting Cycle

Key Fields:

* Initiative Key
* Program Key
* Initiative Name
* Initiative Type
* Owner
* Status

---

## Dim Owner

Examples:

* Fundraiser
* Campaign Manager
* Stewardship Officer
* Director

Key Fields:

* Owner Key
* Name
* Department
* Role

---

## Dim Department

Examples:

* Annual Giving
* Major Gifts
* Stewardship
* Marketing
* Operations

---

## Dim Date

Standard date table.

Required Fields:

* Date
* Month
* Quarter
* Fiscal Month
* Fiscal Quarter
* Fiscal Year

---

## Dim Commitment Type

Examples:

* Donor Follow-Up
* Proposal
* Stewardship
* Operational
* Vendor

---

## Dim Risk Type

Examples:

* Pipeline
* Operational
* Data Quality
* Staffing
* Readiness

---

## Dim Dependency Type

Examples:

* Approval
* Resource
* Technology
* Vendor
* Review

---

## Dim Status

Examples:

* Open
* Complete
* Overdue
* Blocked
* Monitoring
* Resolved

---

# Fact Tables

## Fact Commitments

Purpose:

Track obligations and accountability.

Examples:

* Proposal Due
* Donor Follow-Up
* Stewardship Report
* Sponsor Benefit Delivery

Measures:

* Open Commitments
* Overdue Commitments
* Commitment Completion Rate
* Commitment Aging

---

## Fact Dependencies

Purpose:

Track blockers.

Measures:

* Open Dependencies
* Overdue Dependencies
* High Severity Dependencies
* Average Resolution Time

---

## Fact Risks

Purpose:

Track operational risks.

Measures:

* Open Risks
* High Risks
* Risk Trend
* Risk Resolution Rate

---

## Fact Metric Snapshots

Purpose:

Store historical management metrics.

Examples:

* Readiness Score
* Follow-Up Compliance
* Pipeline Coverage
* Commitment Compliance
* Dependency Count
* Risk Count

Measures:

* Current Value
* Trend
* Variance
* Change Since Last Snapshot

---

# Activity Data

Activities are not core FCC facts.

Activity extracts may be loaded as staging tables.

Examples:

* RE NXT Actions
* Salesforce Tasks
* Planner Tasks

Activity data is primarily used to derive:

* Commitments
* Risks
* Compliance Metrics

---

# Readiness Model

Readiness should be calculated from multiple inputs.

Potential Inputs:

* Open Commitments
* Overdue Commitments
* Open Dependencies
* High Risks
* Required Milestones

Output:

Readiness Score

0-100

Stored in:

Fact Metric Snapshots

---

# Executive Control Tower Metrics

Recommended KPIs:

* Readiness Score
* Open Risks
* Critical Risks
* Open Commitments
* Overdue Commitments
* Follow-Up Compliance
* Dependency Count
* Initiatives At Risk

---

# Work Portfolio Metrics

Recommended KPIs:

* Initiative Status
* Readiness Trend
* Commitment Aging
* Dependency Aging
* Risk Count

---

# Commitments & Follow-Up Metrics

Recommended KPIs:

* Follow-Up Compliance
* Commitments Due This Week
* Commitments Overdue
* Commitments Completed

---

# Dependencies & Risks Metrics

Recommended KPIs:

* Blocked Initiatives
* High Severity Dependencies
* Critical Risks
* Resolution Time

---

# Knowledge Metrics

Recommended KPIs:

* Knowledge Assets
* Assets Due For Review
* Assets Missing Review Owner
* Assets By Program

---

# AI Summary Layer

AI should consume:

* Fact Metric Snapshots
* Fact Risks
* Fact Dependencies
* Fact Commitments

AI should not calculate metrics from raw records.

Power BI remains the calculation engine.

---

# MVP Reports

1. Executive Control Tower

2. Work Portfolio

3. Readiness & Execution

4. Dependencies & Risks

5. Commitments & Follow-Up

6. Knowledgebase

---

# Future Expansion

Future semantic model enhancements may include:

* Forecasting
* Scenario Planning
* Capacity Analysis
* Workload Analysis
* Predictive Risk Scoring
* AI-assisted Recommendations

These are outside MVP scope.

---

# Design Success Criteria

The semantic model succeeds when leadership can answer:

* What is at risk?
* What is overdue?
* What is blocked?
* What requires intervention?

within five minutes of opening the Executive Control Tower.
