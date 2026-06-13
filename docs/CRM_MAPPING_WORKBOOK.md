# CRM_MAPPING_WORKBOOK.md

# Fundraising Command Centre (FCC)

## CRM Mapping Workbook

Version: 2.0

---

# Purpose

This document defines the process used to translate source-system data into the FCC Canonical Data Model.

The purpose of the workbook is not to force a CRM into a predefined structure.

The purpose is to understand how the organization operates and then map that operational reality into FCC.

---

# Core Principle

The Canonical Model is stable.

Source systems are variable.

Different organizations use the same CRM objects differently.

Therefore:

```text
Source Object
≠
Canonical Object
```

There is no guaranteed one-to-one relationship.

Mappings must be explicitly documented.

---

# FCC Canonical Model

FCC manages:

```text
Program
Initiative
Commitment
Dependency
Risk
Knowledge
```

Supporting objects:

```text
Metric Snapshot
Alert
Configuration
Data Quality Issue
```

Activities remain within source systems.

---

# Mapping Methodology

Every implementation follows the same sequence.

```text
Understand Operations
        ↓
Identify Programs
        ↓
Identify Initiatives
        ↓
Identify Commitments
        ↓
Identify Dependencies
        ↓
Identify Risks
        ↓
Identify Knowledge Assets
        ↓
Map Source Data
        ↓
Build Rules
```

---

# Step 1

## Operational Assessment

Before reviewing CRM objects, document how the organization works.

Questions:

* What fundraising functions exist?
* How is work organized?
* How is accountability managed?
* How is readiness monitored?
* How are risks identified?
* How are commitments tracked?

---

# Step 2

## Program Identification

Programs represent strategic fundraising areas.

Examples:

* Annual Giving
* Major Gifts
* Stewardship
* Events
* Corporate Partnerships
* Capital Campaign

Programs are typically leadership-defined constructs.

Programs often do not exist as CRM objects.

---

# Step 3

## Initiative Identification

Initiatives represent operational work portfolios.

Examples:

Annual Giving

* Spring Appeal
* Giving Tuesday
* Year-End Appeal

Major Gifts

* Principal Gifts Portfolio
* Leadership Gifts Portfolio

Events

* Annual Gala
* Golf Tournament

Stewardship

* Impact Reporting Cycle

---

# Step 4

## Source Activity Assessment

Activities remain in source systems.

FCC consumes activities but does not manage them.

---

## Relationship Activities

Examples:

* donor meetings
* qualification calls
* stewardship visits
* proposal discussions

Typical Sources:

* RE NXT Actions
* Salesforce Tasks

---

## Operational Activities

Examples:

* segmentation approval
* venue booking
* creative review
* website deployment

Typical Sources:

* Planner
* Asana
* Smartsheet
* Microsoft Project

---

## Assessment Questions

* Which systems manage activities?
* Are activities consistently recorded?
* Are due dates reliable?
* Are owners reliable?
* Are completion dates reliable?
* Can activities support compliance monitoring?
* Can activities support readiness calculations?

---

# Step 5

## Commitment Identification

Commitments are obligations.

Examples:

* donor follow-up
* proposal deadline
* stewardship report
* campaign launch milestone
* sponsor benefit delivery

Important:

Commitments may originate from:

* CRM
* Planner
* Excel
* Manual entry
* Governance processes

---

# Step 6

## Dependency Identification

Dependencies are blockers.

Examples:

* finance approval
* legal review
* website deployment
* CEO approval
* prospect research

Dependencies rarely exist directly in CRM.

Dependencies are often created through:

* planning tools
* readiness templates
* manual entry

---

# Step 7

## Risk Identification

Risks threaten successful execution.

Examples:

* stalled opportunities
* missing approvals
* overdue commitments
* staffing shortages
* poor readiness

Risks are frequently generated through rules.

---

# Step 8

## Knowledge Identification

Knowledge assets preserve organizational memory.

Examples:

* SOPs
* Policies
* Playbooks
* Templates
* Lessons Learned
* Post-Mortems

Knowledge typically originates in Microsoft 365.

Not CRM.

---

# Source Systems Inventory

Document all systems contributing to FCC.

| System     | Purpose            | System of Record |
| ---------- | ------------------ | ---------------- |
| RE NXT     | CRM                | Yes              |
| Salesforce | CRM                | Yes              |
| Planner    | Task Management    | Yes              |
| Asana      | Task Management    | Yes              |
| Smartsheet | Project Management | Yes              |
| SharePoint | Knowledge          | Yes              |
| Excel      | Operational Data   | Sometimes        |

---

# RE NXT Assessment

The purpose of this section is not to map objects immediately.

The purpose is to understand how RE NXT is used.

---

## Campaign Usage

Questions:

* What does a Campaign represent?
* Is Campaign used consistently?
* Does Campaign align with Programs?
* Does Campaign align with Initiatives?

Document findings.

---

## Appeal Usage

Questions:

* What does an Appeal represent?
* Is Appeal managed consistently?
* Does Appeal align with Initiatives?

Document findings.

---

## Opportunity Usage

Questions:

* Are opportunities actively maintained?
* Are ask dates reliable?
* Are proposal dates reliable?
* Are stages meaningful?
* Do opportunities represent commitments?

Document findings.

---

## Action Usage

Questions:

* Are actions consistently recorded?
* Is next action required?
* Are completion dates reliable?
* Can actions support follow-up compliance?

Document findings.

---

## Portfolio Usage

Questions:

* How are portfolios managed?
* How are assignments maintained?
* Are portfolios reviewed regularly?

Document findings.

---

# Mapping Decision Worksheet

## Program Mapping

| FCC Program   | Source Data            | Notes |
| ------------- | ---------------------- | ----- |
| Annual Giving | Campaigns + Appeals    |       |
| Major Gifts   | Portfolio Structure    |       |
| Stewardship   | Operational Definition |       |

---

## Initiative Mapping

| FCC Initiative            | Source Data         | Notes |
| ------------------------- | ------------------- | ----- |
| Spring Appeal             | Appeal              |       |
| Principal Gifts Portfolio | Portfolio Structure |       |
| Annual Gala               | Event Planning Data |       |

---

## Commitment Mapping

| FCC Commitment | Source Data   | Notes |
| -------------- | ------------- | ----- |
| Proposal Due   | Opportunity   |       |
| Follow-Up Due  | Action        |       |
| Launch Date    | Planning Tool |       |

---

# Data Quality Assessment

Evaluate source-system reliability.

| Area          | High | Medium | Low | Notes |
| ------------- | ---- | ------ | --- | ----- |
| Campaigns     |      |        |     |       |
| Appeals       |      |        |     |       |
| Opportunities |      |        |     |       |
| Actions       |      |        |     |       |
| Portfolios    |      |        |     |       |
| Planner Data  |      |        |     |       |

---

# Mapping Risks

Document implementation concerns.

Examples:

* Opportunities not maintained
* Missing next actions
* Duplicate campaign structures
* Inconsistent appeal naming
* Missing ownership
* Incomplete activity records

---

# Approval

Mappings must be approved before:

* SharePoint build
* Power Automate build
* Power BI semantic model build
* AI summary configuration

Approved By:

---

Date:

---

Version:

---

---

# Success Criteria

The Mapping Workbook succeeds when:

* operational reality is understood
* Programs are clearly defined
* Initiatives are clearly defined
* Commitments are clearly defined
* Dependencies are clearly defined
* Risks are clearly defined
* Knowledge assets are identified
* source-system assumptions are documented

The objective is not CRM standardization.

The objective is accurate operational translation into the FCC Canonical Model.
