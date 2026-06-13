# CANONICAL_DATA_MODEL.md

# Fundraising Command Centre (FCC)

## Canonical Data Model

Version: 2.0

---

# Purpose

This document defines the canonical operational data model used by the Fundraising Command Centre (FCC).

The model is intentionally independent of:

* CRM systems
* Fundraising platforms
* Project management systems
* Marketing platforms
* Reporting platforms

The Canonical Data Model serves as the foundation for:

* SharePoint Lists
* Power BI Semantic Model
* Power Automate Rules
* AI Summaries
* Future Integrations

---

# Design Philosophy

FCC is an operational intelligence platform.

FCC is not:

* a CRM
* a project management system
* a marketing platform
* a fundraising platform

FCC provides leadership visibility into execution, accountability, readiness, dependencies, risks, and organizational knowledge.

---

# Critical Design Principle

The Canonical Model is stable.

Mappings are variable.

No source-system object has a guaranteed one-to-one relationship with a canonical FCC object.

Examples:

An RE NXT Opportunity may represent:

* a Commitment
* an Initiative
* both
* neither

depending on how the organization operates.

All mappings must be documented through:

CRM_MAPPING_WORKBOOK.md

---

# Canonical Object Hierarchy

FCC is built around the following hierarchy:

```text
Program
    ↓
Initiative
```

Supporting operational objects:

```text
Commitment
Dependency
Risk
Knowledge
```

Supporting system objects:

```text
Metric Snapshot
Alert
Configuration
Data Quality Issue
```

---

# Program

## Definition

A strategic fundraising area that groups related operational work.

Programs represent how leadership views fundraising operations.

Programs are FCC-owned objects.

---

## Examples

* Annual Giving
* Major Gifts
* Stewardship
* Events
* Corporate Partnerships
* Capital Campaign

---

## Purpose

Programs provide:

* strategic organization
* executive reporting
* ownership structure
* portfolio grouping

---

## Required Attributes

| Field           | Description            |
| --------------- | ---------------------- |
| Program ID      | Unique identifier      |
| Program Name    | Program name           |
| Program Type    | Category               |
| Executive Owner | Senior leader          |
| Department      | Responsible department |
| Status          | Active / Inactive      |
| Start Date      | Program start          |
| End Date        | Program end            |

---

# Initiative

## Definition

A managed operational work portfolio within a Program.

Initiatives are the primary unit of management within FCC.

---

## Examples

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
* Donor Recognition Program

---

## Purpose

Initiatives provide:

* operational accountability
* readiness tracking
* risk management
* commitment management

---

## Required Attributes

| Field           | Description                             |
| --------------- | --------------------------------------- |
| Initiative ID   | Unique identifier                       |
| Initiative Name | Initiative title                        |
| Program ID      | Parent Program                          |
| Initiative Type | Portfolio, Appeal, Event, Program Cycle |
| Owner           | Responsible individual                  |
| Status          | Active, Complete, On Hold               |
| Start Date      | Initiative start                        |
| Target Date     | Initiative target date                  |
| Readiness Score | Calculated metric                       |
| Risk Score      | Calculated metric                       |

---

# Activity Strategy

Activities are intentionally not FCC-owned objects.

Activities remain within their source systems.

FCC consumes activity information but does not become the system of record for activity management.

---

## Relationship Activities

Examples:

* donor meetings
* qualification calls
* stewardship visits
* proposal discussions
* follow-up calls

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
* sponsorship package review

Typical Sources:

* Planner
* Asana
* Smartsheet
* Microsoft Project

---

## FCC Use of Activities

Activities may contribute to:

* readiness calculations
* commitment monitoring
* follow-up compliance
* dependency detection
* risk generation

Activities are considered source data rather than FCC-managed records.

---

# Commitment

## Definition

A commitment represents an obligation that must be fulfilled.

Commitments are one of the primary accountability objects within FCC.

---

## Examples

* donor follow-up
* proposal due
* stewardship report
* campaign launch milestone
* sponsor benefit delivery
* executive briefing

---

## Purpose

Commitments allow leadership to monitor:

* accountability
* overdue work
* execution discipline
* operational readiness

---

## Required Attributes

| Field            | Description              |
| ---------------- | ------------------------ |
| Commitment ID    | Unique identifier        |
| Commitment Name  | Commitment title         |
| Initiative ID    | Related Initiative       |
| Commitment Type  | Category                 |
| Owner            | Responsible individual   |
| Due Date         | Commitment due date      |
| Status           | Open, Completed, Overdue |
| Priority         | Priority level           |
| Value Amount     | Associated value         |
| Escalation Level | None, Manager, Director  |
| Source System    | Originating system       |
| Source Record ID | Reference identifier     |

Commitments link to an Initiative only. The parent Program is inferred by following the Initiative's Program reference. No direct Program link is stored on Commitments.

---

# Dependency

## Definition

A dependency is a prerequisite that must be completed before another activity, commitment, or initiative can proceed.

Dependencies are a key differentiator of FCC.

---

## Examples

* finance approval
* legal review
* CEO briefing
* website deployment
* prospect research completion

---

## Purpose

Dependencies allow leadership to identify:

* bottlenecks
* blockers
* approval delays
* execution risks

---

## Required Attributes

| Field              | Description                          |
| ------------------ | ------------------------------------ |
| Dependency ID      | Unique identifier                    |
| Dependency Name    | Dependency title                     |
| Initiative ID      | Related Initiative                   |
| Dependency Type    | Category (Approval, Resource, etc.)  |
| Blocking Area      | Department or function causing block |
| Impacted Area      | Department or function blocked       |
| Owner              | Responsible individual               |
| Due Date           | Required completion date             |
| Status             | Open, Resolved                       |
| Severity           | Low, Medium, High                    |
| Impact Description  | Narrative description of impact      |

A Dependency records both a categorical Dependency Type and the specific Blocking Area / Impacted Area involved. The Type supports dimensional reporting; the Areas identify which functions are blocking and blocked. Dependencies link to an Initiative only; the parent Program is inferred via the Initiative.

---

# Risk

## Definition

A condition that threatens successful execution.

Risks may be manually entered or system generated.

---

## Examples

* stalled opportunity
* overdue commitment
* missing approval
* low readiness score
* resource shortage
* data quality issue

---

## Purpose

Risks allow leadership to focus attention where intervention is required.

---

## Required Attributes

| Field           | Description                |
| --------------- | -------------------------- |
| Risk ID         | Unique identifier          |
| Risk Name       | Risk title                 |
| Initiative ID   | Related Initiative         |
| Risk Type       | Category                   |
| Severity        | Low, Medium, High          |
| Likelihood      | Low, Medium, High          |
| Status          | Open, Monitoring, Resolved |
| Owner           | Responsible individual     |
| Mitigation Plan | Resolution approach        |

Risks link to an Initiative only; the parent Program is inferred via the Initiative. Risks may be manually entered or generated by the Rules Layer.

---

# Knowledge

## Definition

Institutional knowledge required to support fundraising operations.

Knowledge assets preserve organizational memory.

---

## Examples

* SOPs
* Policies
* Playbooks
* Templates
* Lessons Learned
* Decision Logs
* Post-Mortems

---

## Purpose

Knowledge supports:

* onboarding
* consistency
* compliance
* organizational learning

---

## Required Attributes

| Field            | Description                 |
| ---------------- | --------------------------- |
| Knowledge ID     | Unique identifier           |
| Title            | Asset title                 |
| Type             | SOP, Policy, Template, etc. |
| Owner            | Responsible individual      |
| Status           | Draft, Approved, Archived   |
| Review Date      | Next review date            |
| Source Authority | Working, Approved, Official |

---

# Supporting Objects

## Metric Snapshot

Stores historical operational metrics.

Examples:

* Readiness Score
* Follow-Up Compliance
* Open Risks
* Open Commitments
* Dependency Count
* Pipeline Coverage

Metric Snapshots are preferred inputs for Power BI and AI summaries.

---

## Alert

Stores generated operational notifications.

Examples:

* overdue commitment
* stalled prospect
* readiness decline
* critical dependency

---

## Configuration

Stores client-specific settings.

Examples:

* SLA thresholds
* readiness weights
* escalation rules
* scoring formulas

---

## Data Quality Issue

Stores identified data quality concerns.

Examples:

* missing owner
* missing due date
* duplicate record
* missing next action

---

# Object Relationships

```text
Program
    ↓
Initiative

Initiative
    ↓
Commitments

Initiative
    ↓
Dependencies

Initiative
    ↓
Risks

Initiative
    ↓
Knowledge

Initiative
    ↓
Metric Snapshots
```

Activities remain outside FCC and feed operational intelligence through source-system integrations.

---

# Design Success Criteria

The Canonical Model succeeds when:

* it supports multiple fundraising disciplines
* it does not require separate architectures for different teams
* it supports both relationship-based and project-based fundraising work
* it remains independent of specific CRM implementations
* it provides a stable foundation for Power BI, Power Automate, AI, and future integrations

The Canonical Model is intended to be the long-term foundation of the Fundraising Command Centre platform.
