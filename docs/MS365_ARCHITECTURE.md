# MS365_ARCHITECTURE.md

# Fundraising Command Centre (FCC)

## Microsoft 365 Architecture

Version: 1.0

---

# Purpose

This document defines the Microsoft 365 architecture used to implement the Fundraising Command Centre.

The architecture is designed around the FCC Canonical Data Model and Mapping Methodology.

FCC is implemented as an operational intelligence layer above CRM, planning, fundraising, and collaboration systems.

---

# Architectural Principles

## Principle 1

CRM remains the source of donor truth.

Examples:

* RE NXT
* Salesforce
* DonorPerfect

FCC does not replace CRM.

---

## Principle 2

Planning systems remain the source of task truth.

Examples:

* Planner
* Asana
* Smartsheet
* Microsoft Project

FCC does not replace project management tools.

---

## Principle 3

FCC owns operational intelligence.

FCC manages:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Knowledge
* Metrics
* Alerts

---

## Principle 4

Activity data is consumed, not duplicated.

Activities remain in source systems.

FCC uses activity data to calculate:

* readiness
* compliance
* risk
* workload
* follow-up discipline

---

# Architecture Overview

```text
CRM Systems
(RE NXT, Salesforce)

Planning Systems
(Planner, Asana, Smartsheet)

Knowledge Sources
(SharePoint, Teams)

              ↓

      Data Ingestion Layer

              ↓

      FCC Operational Layer

              ↓

      Metrics & Rules Layer

              ↓

      Power BI

              ↓

      Teams & AI Summaries
```

---

# Microsoft 365 Components

## SharePoint

Primary operational datastore.

Stores:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Configuration
* Metric Snapshots

---

## Document Libraries

### Data Drop

Purpose:

Store imported files.

Examples:

* RE NXT exports
* Salesforce exports
* Planner exports
* Excel uploads

Structure:

Data Drop
CRM
Planning
Finance
Other

---

### Knowledge Library

Purpose:

Store operational knowledge assets.

Examples:

* SOPs
* Policies
* Playbooks
* Templates
* Post-Mortems
* Lessons Learned

---

## Power Automate

Purpose:

Transform data into operational intelligence.

Responsibilities:

* Data ingestion
* Readiness scoring
* Risk generation
* Alert generation
* Snapshot creation
* Weekly digest preparation

---

## Power BI

Purpose:

Operational visibility.

Power BI is the primary user interface.

---

## Teams

Purpose:

Operational review and action.

Teams receives:

* alerts
* digests
* escalation notices
* review materials

---

# SharePoint Lists

## Programs

Stores strategic fundraising areas.

Examples:

* Annual Giving
* Major Gifts
* Events
* Stewardship

---

## Initiatives

Stores operational work portfolios.

Examples:

* Spring Appeal
* Year-End Appeal
* Annual Gala
* Principal Gifts Portfolio

---

## Commitments

Stores operational obligations.

Examples:

* proposal due
* stewardship report
* launch milestone
* sponsor benefit delivery

---

## Dependencies

Stores operational blockers.

Examples:

* finance approval
* legal review
* website deployment

---

## Risks

Stores identified risks.

Examples:

* stalled prospects
* overdue commitments
* launch readiness concerns

---

## Metric Snapshots

Stores periodic calculations.

Examples:

* readiness score
* pipeline coverage
* follow-up compliance
* risk score

---

## Configuration

Stores:

* thresholds
* scoring weights
* escalation rules
* SLA definitions

---

# Data Ingestion Strategy

Phase 1:

CSV-based ingestion.

Supported sources:

* RE NXT exports
* Planner exports
* Excel uploads

No API integrations required.

---

# Activity Integration Strategy

FCC does not maintain a master activity table.

Activities remain in source systems.

Examples:

Relationship Activities

* RE NXT Actions
* Salesforce Tasks

Operational Activities

* Planner Tasks
* Asana Tasks
* Smartsheet Tasks

FCC consumes activity information to generate:

* Commitments
* Risks
* Readiness indicators
* Compliance metrics

---

# Rules Layer

The Rules Layer creates operational intelligence.

Examples:

No activity for 90 days
→ Stalled Prospect Risk

Proposal overdue
→ Commitment Alert

Missing readiness item
→ Readiness Reduction

Blocked dependency
→ Operational Risk

---

# Power BI Pages

## Executive Control Tower

Executive visibility.

---

## Work Portfolio

Program and Initiative management.

---

## Readiness & Execution

Readiness monitoring.

---

## Dependencies & Risks

Blockers and risk management.

---

## Commitments & Follow-Up

Accountability monitoring.

---

## Knowledgebase

Operational knowledge management.

---

# AI Layer

AI receives:

* Metric Snapshots
* Risks
* Commitments
* Readiness Scores

AI does not calculate KPIs.

AI provides:

* weekly digest
* executive briefing
* readiness narrative
* risk summary

---

# Security Model

CRM remains system of record.

FCC minimizes donor PII.

Store:

* source system
* source record ID
* owner
* status
* dates
* metrics

Avoid:

* detailed donor notes
* contact information
* sensitive donor information

---

# MVP Scope

Phase 1 includes:

* SharePoint Lists
* Document Libraries
* CSV imports
* Power Automate
* Power BI
* Teams integration
* AI summaries

Phase 1 excludes:

* write-back to CRM
* custom application development
* multi-CRM integration framework
* standalone SaaS platform

---

# Future Architecture

Future versions may support:

* live API integrations
* Salesforce
* RE NXT SKY API
* Dataverse
* Copilot Studio
* standalone SaaS deployment

The Microsoft 365 implementation serves as the reference architecture for all future versions of FCC.

