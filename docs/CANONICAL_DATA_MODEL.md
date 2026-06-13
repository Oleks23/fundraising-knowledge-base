# CANONICAL_DATA_MODEL.md

# Fundraising Command Centre (FCC)

## Canonical Data Model

Version: 1.0

---
# Warning

The examples in this document illustrate the intent of the model.

They are not implementation rules.

Actual mappings between source systems and canonical objects must be documented in CRM_MAPPING_WORKBOOK.md and may vary by organization.

# Purpose

This document defines the canonical operational data model used by the Fundraising Command Centre (FCC).

The canonical model is intentionally independent of:

* CRM systems
* Project management systems
* Marketing platforms
* Giving platforms
* Analytics platforms

All source systems are mapped into the canonical model through a separate Mapping Workbook.

The canonical model is the foundation for:

* SharePoint Lists
* Power BI semantic model
* Power Automate rules
* AI summaries
* Future API integrations

---

# Critical Design Principle

The canonical model is stable.

Source-system mappings are variable.

There is no assumption that:

```text
CRM Object A
=
Canonical Object B
```

for every client.

Different organizations use CRM objects differently.

Examples:

* RE NXT Opportunities may map to Commitments, Initiatives, or both.
* Salesforce Campaigns may represent Appeals, Events, or entire Campaign Programs.
* Planner Tasks may represent Activities or Readiness Items.
* Stewardship Obligations may originate from CRM, Excel, or SharePoint.

All mappings must be explicitly documented.

The Mapping Workbook is therefore a required implementation artifact.

---

# Canonical Object Overview

FCC is built around seven operational objects:

```text
Programs
Initiatives
Dependencies
Commitments
Risks
Knowledge

```

Supporting objects:

```text
Metric Snapshots
Configuration
Alerts
Data Quality Issues
Source Activities
Relationship Activities
Operational Activities
```

---
# Program / Initiative Hierarchy

FCC supports a hierarchy:

Program → Initiative → Activity

## Program

A Program is a higher-level fundraising area or campaign grouping.

Examples:

- Annual Giving
- Major Gifts
- Events
- Corporate Giving
- Stewardship
- Capital Campaign
- FY2027 Direct Marketing Campaign

Programs are useful for executive grouping, portfolio reporting, and strategic oversight.

## Initiative

An Initiative is the actual managed work object.

Examples:

- Spring Appeal
- Year-End Appeal
- Annual Gala
- Principal Gifts Portfolio
- Monthly Donor Upgrade Campaign
- Foundation Stewardship Reporting Cycle

In many cases, the Initiative is the object that has readiness, commitments, dependencies, risks, and activities.

## Activity

An Activity is a specific unit of work required to execute the Initiative.

Examples:

- Approve segmentation
- Finalize creative
- Confirm finance coding
- Conduct donor meeting
- Prepare proposal
- Deliver impact report

## Important Mapping Note

Source-system terms such as Campaign, Appeal, Fund, Opportunity, Portfolio, and Event should not be mapped mechanically.

For example, in RE NXT:

- Campaign may map to Program
- Appeal may map to Initiative
- Opportunity may map to Commitment or Initiative depending on client usage
- Fund may map to Initiative Attribute or Financial Designation
- Action may map to Activity

Mappings must be confirmed in CRM_MAPPING_WORKBOOK.md.

# 1. Initiative

## Definition

A managed fundraising work portfolio.

An Initiative represents a body of work that leadership wants to monitor and manage.

Initiatives contain Activities, Dependencies, Commitments, Risks, and Metrics.

---

## Examples

Direct Response

* Spring Appeal
* Year-End Appeal
* Monthly Giving Program

Major Gifts

* Principal Gifts Portfolio
* Mid-Level Giving Program

Events

* Annual Gala
* Golf Tournament

Stewardship

* Donor Reporting Program
* Naming Recognition Program

Campaigns

* Capital Campaign
* Campaign Quiet Phase

---

## Required Fields

| Field           | Description                                 |
| --------------- | ------------------------------------------- |
| Initiative ID   | Unique identifier                           |
| Title           | Initiative name                             |
| Type            | Campaign, Appeal, Event, Portfolio, Program |
| Status          | Planning, Active, Completed, On Hold        |
| Owner           | Responsible person                          |
| Department      | Primary department                          |
| Start Date      | Start date                                  |
| Target Date     | Target completion date                      |
| Readiness Score | Calculated                                  |
| Risk Score      | Calculated                                  |

---

# 2. Activity

## Definition

A unit of work required to advance an Initiative.

Activities are actionable items.

---

## Examples

* Secure lead sponsor
* Create case for support
* Approve segmentation
* Conduct donor meeting
* Draft proposal
* Review stewardship report

---

## Required Fields

| Field            | Description                                 |
| ---------------- | ------------------------------------------- |
| Activity ID      | Unique identifier                           |
| Initiative ID    | Parent initiative                           |
| Title            | Activity name                               |
| Description      | Activity description                        |
| Owner            | Responsible individual                      |
| Status           | Not Started, In Progress, Complete, Blocked |
| Priority         | Low, Medium, High                           |
| Due Date         | Required completion date                    |
| Source System    | Originating system                          |
| Source Record ID | External identifier                         |

---

# 3. Dependency

## Definition

A relationship where completion of one activity depends upon another activity, decision, deliverable, approval, or external event.

Dependencies are a major differentiator of FCC.

---

## Examples

* Finance approval required before launch
* Legal review required before sponsorship package
* Website deployment required before campaign launch
* Research profile required before solicitation

---

## Required Fields

| Field         | Description                    |
| ------------- | ------------------------------ |
| Dependency ID | Unique identifier              |
| Initiative ID | Related initiative             |
| Blocking Item | What is causing the dependency |
| Impacted Item | What is blocked                |
| Owner         | Resolution owner               |
| Due Date      | Required resolution date       |
| Status        | Open, Resolved                 |
| Severity      | Low, Medium, High              |

---

# 4. Commitment

## Definition

An obligation that must be fulfilled.

Commitments are accountability objects.

---

## Examples

* Donor follow-up due
* Stewardship report due
* Proposal submission deadline
* Sponsorship benefit delivery
* Campaign launch milestone

---

## Required Fields

| Field            | Description                             |
| ---------------- | --------------------------------------- |
| Commitment ID    | Unique identifier                       |
| Initiative ID    | Related initiative                      |
| Title            | Commitment description                  |
| Owner            | Responsible person                      |
| Due Date         | Due date                                |
| Status           | Open, Completed, Overdue                |
| Commitment Type  | Donor, Stewardship, Operational, Vendor |
| Escalation Level | None, Manager, Director                 |

---

# 5. Risk

## Definition

A condition that threatens successful execution.

Risks can be operational, financial, data-related, staffing-related, or fundraising-related.

---

## Examples

* Stalled prospect pipeline
* Missing readiness items
* Data quality issue
* Resource shortage
* Delayed approval

---

## Required Fields

| Field         | Description                            |
| ------------- | -------------------------------------- |
| Risk ID       | Unique identifier                      |
| Initiative ID | Related initiative                     |
| Risk Type     | Operational, Data, Financial, Staffing |
| Description   | Risk description                       |
| Severity      | Low, Medium, High                      |
| Likelihood    | Low, Medium, High                      |
| Status        | Open, Monitoring, Resolved             |
| Owner         | Risk owner                             |

---

# 6. Knowledge

## Definition

Institutional knowledge supporting fundraising operations.

Knowledge assets preserve organizational memory.

---

## Examples

* SOP
* Playbook
* Policy
* Template
* Decision Log
* Lessons Learned
* Post-Mortem

---

## Required Fields

| Field            | Description                     |
| ---------------- | ------------------------------- |
| Knowledge ID     | Unique identifier               |
| Title            | Asset title                     |
| Type             | SOP, Policy, Template, Playbook |
| Module           | Related operational area        |
| Owner            | Document owner                  |
| Review Date      | Next review                     |
| Status           | Draft, Approved, Archived       |
| Source Authority | Working, Approved, Official     |

---

# Supporting Objects

## Metric Snapshot

Stores periodic calculated metrics.

Examples:

* Readiness Score
* Pipeline Coverage
* Stalled Prospect Count
* Follow-Up Compliance
* Open Dependencies
* Open Risks

Metric Snapshots are the preferred AI input.

---

## Data Quality Issue

Tracks data problems detected during ingestion.

Examples:

* Missing next action
* Missing owner
* Missing stage
* Invalid date
* Duplicate record

---

## Alert

Tracks operational notifications.

Examples:

* Overdue commitment
* Stalled prospect
* High-risk dependency
* Readiness decline

---

## Configuration

Stores client-specific settings.

Examples:

* Readiness scoring weights
* SLA thresholds
* Risk thresholds
* Escalation rules
* Department list

---

# Mapping Principles

The canonical model is not a CRM model.

The canonical model is not a project management model.

The canonical model is an operational execution model.

All CRM, project management, marketing, and giving systems are translated into this model through implementation-specific mappings.

Mappings must be documented separately within:

CRM_MAPPING_WORKBOOK.md

No implementation may assume that a source-system object always maps to the same canonical object.

Mappings must be reviewed and approved during implementation.

