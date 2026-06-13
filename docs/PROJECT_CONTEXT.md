# PROJECT_CONTEXT.md

# Fundraising Command Centre (FCC)

Version: 2.0

---

# Project Overview

Fundraising Command Centre (FCC) is a Microsoft 365-based operational intelligence platform for fundraising organizations.

FCC provides leadership visibility into:

* execution
* readiness
* commitments
* dependencies
* risks
* knowledge
* operational performance

FCC sits above CRM systems, planning tools, fundraising platforms, and reporting systems.

FCC is designed to answer:

* Are we on track?
* What is at risk?
* What is overdue?
* What is blocked?
* What requires intervention?

within minutes.

---

# Design Maturity

The project is currently in the architecture and validation phase.

The Canonical Data Model, Mapping Methodology, and Microsoft 365 Architecture have been established but continue to evolve through scenario testing and implementation planning.

Examples within project documentation are illustrative.

They are not implementation rules.

Implementation-specific decisions must be documented and approved through the CRM Mapping Workbook.

---

# Vision

Most fundraising organizations possess:

* CRM systems
* fundraising platforms
* marketing systems
* project management tools
* Microsoft 365
* reporting platforms

However, they lack a unified operational management layer.

FCC fills that gap.

FCC provides a common operational framework across fundraising disciplines while allowing each team to continue using its preferred operational systems.

---

# Product Philosophy

CRM manages donor relationships.

Project management systems manage tasks.

Power BI manages reporting.

FCC manages operational accountability.

---

# Strategic Design Principle

FCC does not attempt to replace:

* RE NXT
* Salesforce
* Planner
* Asana
* Smartsheet
* Project

Instead FCC consumes information from these systems and converts it into operational intelligence.

---

# Universal Work Model

The FCC Canonical Model is built around six core operational objects.

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
Configuration
Alert
Data Quality Issue
```

---

# Program

Programs represent strategic fundraising areas.

Examples:

* Annual Giving
* Major Gifts
* Events
* Stewardship
* Corporate Partnerships

Programs are typically defined by leadership.

Programs are FCC-owned objects.

---

# Initiative

Initiatives represent managed work portfolios.

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

* Foundation Reporting Program
* Impact Reporting Cycle

Initiatives are FCC-owned objects.

---

# Activity Management Principle

Activities are not FCC-owned objects.

Activities remain within their operational systems.

Examples:

Relationship Activities

* donor meetings
* qualification calls
* stewardship visits
* proposal discussions

Sources:

* RE NXT Actions
* Salesforce Tasks

Operational Activities

* segmentation approval
* venue coordination
* website deployment
* creative review

Sources:

* Planner
* Asana
* Smartsheet
* Microsoft Project

FCC consumes activity information but does not become the system of record for activities.

---

# Commitments

Commitments represent obligations that must be fulfilled.

Examples:

* donor follow-up
* proposal deadline
* stewardship report
* campaign launch milestone
* sponsor benefit delivery

Commitments are a primary FCC-managed object.

---

# Dependencies

Dependencies represent blockers and prerequisites.

Examples:

* finance approval
* legal review
* CEO briefing
* website deployment
* prospect research

Dependencies are a primary FCC-managed object.

---

# Risks

Risks represent conditions that threaten successful execution.

Examples:

* stalled opportunities
* overdue commitments
* missing approvals
* resource constraints
* data quality issues

Risks are a primary FCC-managed object.

---

# Knowledge

Knowledge preserves institutional memory.

Examples:

* SOPs
* policies
* playbooks
* templates
* lessons learned
* post-mortems

Knowledge is a primary FCC-managed object.

---

# Mapping Philosophy

The Canonical Model is stable.

Mappings are variable.

No source-system object has a guaranteed one-to-one relationship with a canonical FCC object.

Examples:

RE NXT Opportunity

may map to:

* Commitment
* Initiative
* Both

depending on organizational practices.

All mappings must be documented through:

CRM_MAPPING_WORKBOOK.md

---

# Primary Platform

Version 1 implementation uses Microsoft 365.

Core technologies:

* SharePoint Lists
* SharePoint Document Libraries
* Power Automate
* Power BI
* Teams

Optional:

* Azure OpenAI
* Copilot
* Copilot Studio

---

# SharePoint Architecture

FCC owns:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Knowledge Metadata
* Metric Snapshots
* Configuration

FCC does not own:

* CRM Actions
* Planner Tasks
* Project Plans

---

# Power BI Architecture

Power BI serves as the primary user interface for FCC.

Primary pages:

* Executive Control Tower
* Work Portfolio
* Readiness & Execution
* Dependencies & Risks
* Commitments & Follow-Up
* Knowledgebase

Power BI is designed around management questions rather than source-system tables.

---

# CRM Strategy

Initial target:

* Raiser's Edge NXT

Future targets:

* Salesforce Nonprofit Cloud
* Salesforce NPSP
* DonorPerfect
* Keela

CRM remains the source of donor truth.

FCC remains the source of operational intelligence.

---

# Data Principles

FCC minimizes donor PII.

Store:

* source system
* source record ID
* owner
* dates
* statuses
* metrics

Avoid:

* detailed donor notes
* contact information
* unnecessary donor data

---

# AI Principles

AI assists with interpretation.

AI does not become the source of truth.

AI receives:

* Metric Snapshots
* Risks
* Dependencies
* Commitments

AI outputs:

* executive summaries
* readiness summaries
* risk narratives
* weekly digests

AI should not calculate KPIs from raw records.

---

# MVP Scope

Included:

* SharePoint Lists
* SharePoint Libraries
* CSV ingestion
* RE NXT reference implementation
* Power Automate rules
* Power BI dashboards
* Teams integration
* AI summaries

Excluded:

* live CRM write-back
* SaaS platform
* multi-CRM framework
* predictive analytics
* Dataverse implementation

---

# Definition of Success

FCC succeeds when fundraising leadership can answer:

* What is at risk?
* What is overdue?
* What is blocked?
* What requires intervention?

within five minutes of opening the Executive Control Tower.

---

# Repository Structure

/docs

* PROJECT_CONTEXT.md
* CANONICAL_DATA_MODEL.md
* CRM_MAPPING_WORKBOOK.md
* MS365_ARCHITECTURE.md
* SHAREPOINT_LISTS_DESIGN.md
* POWER_BI_SEMANTIC_MODEL.md
* ROADMAP.md
* RE_NXT_REFERENCE_IMPLEMENTATION.md
* MVP_SCENARIO_VALIDATION.md

This document serves as the authoritative project overview and should be reviewed before making architectural, implementation, or product decisions.
