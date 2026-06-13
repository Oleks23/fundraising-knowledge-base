# SHAREPOINT_LISTS_DESIGN.md

# Fundraising Command Centre

## SharePoint Lists Design

Version: 1.0

---

# Purpose

This document defines the SharePoint Lists required for the Microsoft 365 MVP of the Fundraising Command Centre.

FCC does not duplicate CRM actions or planning-tool tasks.

FCC owns operational oversight records:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Knowledge
* Metric Snapshots
* Configuration

---

# Core Lists

## 1. Programs

Purpose:

Stores high-level fundraising areas.

Examples:

* Annual Giving
* Major Gifts
* Events
* Stewardship
* Corporate Partnerships

Key Columns:

| Column          | Type                |
| --------------- | ------------------- |
| Program ID      | Single line text    |
| Program Name    | Single line text    |
| Program Type    | Choice              |
| Executive Owner | Person              |
| Department      | Choice              |
| Status          | Choice              |
| Strategic Goal  | Multiple lines text |
| Start Date      | Date                |
| End Date        | Date                |

---

## 2. Initiatives

Purpose:

Stores managed fundraising work portfolios under Programs.

Examples:

* Spring Appeal
* Year-End Appeal
* Principal Gifts Portfolio
* Annual Gala
* Impact Reporting Cycle

Key Columns:

| Column           | Type               |
| ---------------- | ------------------ |
| Initiative ID    | Single line text   |
| Initiative Name  | Single line text   |
| Program          | Lookup to Programs |
| Initiative Type  | Choice             |
| Owner            | Person             |
| Department       | Choice             |
| Status           | Choice             |
| Start Date       | Date               |
| Target Date      | Date               |
| Goal Amount      | Currency           |
| Readiness Score  | Number             |
| Risk Score       | Number             |
| Source System    | Choice             |
| Source Record ID | Single line text   |

---

## 3. Commitments

Purpose:

Stores obligations requiring follow-up or completion.

Examples:

* Proposal due
* Donor follow-up
* Stewardship report
* Sponsor benefit delivery
* Campaign launch date

Key Columns:

| Column           | Type                  |
| ---------------- | --------------------- |
| Commitment ID    | Single line text      |
| Commitment Name  | Single line text      |
| Program          | Lookup to Programs    |
| Initiative       | Lookup to Initiatives |
| Commitment Type  | Choice                |
| Owner            | Person                |
| Due Date         | Date                  |
| Status           | Choice                |
| Priority         | Choice                |
| Value Amount     | Currency              |
| Source System    | Choice                |
| Source Record ID | Single line text      |
| Escalation Level | Choice                |
| Notes            | Multiple lines text   |

---

## 4. Dependencies

Purpose:

Stores blockers and cross-functional dependencies.

Examples:

* Finance approval
* Legal review
* Website deployment
* Prospect research required

Key Columns:

| Column            | Type                  |
| ----------------- | --------------------- |
| Dependency ID     | Single line text      |
| Dependency Name   | Single line text      |
| Program           | Lookup to Programs    |
| Initiative        | Lookup to Initiatives |
| Blocking Area     | Choice                |
| Impacted Area     | Choice                |
| Owner             | Person                |
| Due Date          | Date                  |
| Status            | Choice                |
| Severity          | Choice                |
| Downstream Impact | Multiple lines text   |
| Resolution Notes  | Multiple lines text   |

---

## 5. Risks

Purpose:

Stores operational risks, whether manually entered or system-generated.

Examples:

* Stalled prospect
* Overdue commitment
* Campaign launch risk
* Missing owner
* Data quality issue

Key Columns:

| Column                 | Type                  |
| ---------------------- | --------------------- |
| Risk ID                | Single line text      |
| Risk Name              | Single line text      |
| Program                | Lookup to Programs    |
| Initiative             | Lookup to Initiatives |
| Risk Type              | Choice                |
| Severity               | Choice                |
| Likelihood             | Choice                |
| Status                 | Choice                |
| Owner                  | Person                |
| Date Identified        | Date                  |
| Target Resolution Date | Date                  |
| Source                 | Choice                |
| Source Record ID       | Single line text      |
| Mitigation Plan        | Multiple lines text   |

---

## 6. Knowledge

Purpose:

Stores indexed operational knowledge assets.

The actual documents live in a SharePoint Document Library.

This list stores metadata.

Examples:

* SOP
* Policy
* Playbook
* Template
* Post-mortem
* Decision log

Key Columns:

| Column           | Type                     |
| ---------------- | ------------------------ |
| Knowledge ID     | Single line text         |
| Title            | Single line text         |
| Knowledge Type   | Choice                   |
| Program          | Lookup to Programs       |
| Initiative       | Lookup to Initiatives    |
| Owner            | Person                   |
| Status           | Choice                   |
| Source Authority | Choice                   |
| Review Date      | Date                     |
| Document Link    | Hyperlink                |
| Tags             | Managed metadata or text |

---

## 7. Metric Snapshots

Purpose:

Stores calculated metrics over time.

This is the preferred input to Power BI and AI summaries.

Examples:

* Readiness Score
* Open Risks
* Overdue Commitments
* Follow-Up Compliance
* Dependency Count

Key Columns:

| Column           | Type                  |
| ---------------- | --------------------- |
| Snapshot ID      | Single line text      |
| Snapshot Date    | Date                  |
| Program          | Lookup to Programs    |
| Initiative       | Lookup to Initiatives |
| Metric Name      | Choice or text        |
| Metric Value     | Number                |
| Metric Unit      | Choice                |
| Threshold Status | Choice                |
| Source           | Choice                |
| Notes            | Multiple lines text   |

---

## 8. Configuration

Purpose:

Stores client-specific rules and thresholds.

Examples:

* Follow-up SLA days
* Risk thresholds
* Readiness score weights
* Escalation rules

Key Columns:

| Column         | Type                |
| -------------- | ------------------- |
| Config ID      | Single line text    |
| Config Area    | Choice              |
| Config Name    | Single line text    |
| Config Value   | Single line text    |
| Effective Date | Date                |
| Status         | Choice              |
| Notes          | Multiple lines text |

---

# Document Libraries

## Data Drop Library

Purpose:

Stores imported source-system files.

Folders:

* CRM
* Planning
* Finance
* Events
* Stewardship
* Other

Examples:

* RE NXT opportunities export
* RE NXT actions export
* Planner tasks export
* Smartsheet export

---

## Knowledge Library

Purpose:

Stores operational documents.

Folders:

* SOPs
* Policies
* Playbooks
* Templates
* Post-Mortems
* Decision Logs

---

# Activity Handling

Activities are not stored as FCC-owned records in the MVP.

Relationship activities remain in CRM.

Examples:

* RE NXT Actions
* Salesforce Tasks

Operational activities remain in planning tools.

Examples:

* Planner
* Asana
* Smartsheet
* Microsoft Project

FCC imports or references activity data to generate:

* Commitment status
* Follow-up compliance
* Readiness score
* Risks
* Metric Snapshots

---

# Design Decision

The MVP intentionally avoids a custom Activities List.

Reason:

Creating a universal Activities List would duplicate CRM actions and project-management tasks.

FCC should monitor execution, not replace execution systems.

---

# Power BI Implications

Power BI should model:

Dimensions:

* Program
* Initiative
* Department
* Owner
* Date
* Status
* Risk Type
* Commitment Type

Facts:

* Commitments
* Dependencies
* Risks
* Metric Snapshots

Imported activity extracts may appear as staging tables, not core FCC facts.

---

# MVP Success Criteria

The SharePoint structure succeeds if users can:

* View Programs and Initiatives
* Track Commitments
* Track Dependencies
* Track Risks
* Store Knowledge assets
* Generate Metric Snapshots
* Feed Power BI dashboards
* Support weekly Teams review

without duplicating CRM or planning-tool task management.
