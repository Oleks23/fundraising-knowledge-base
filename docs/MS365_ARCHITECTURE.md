# MS365_ARCHITECTURE.md

# Fundraising Command Centre (FCC)

## Microsoft 365 Architecture

Version: 2.0

---

# Purpose

This document defines the Microsoft 365 architecture used to implement the Fundraising Command Centre (FCC).

The architecture supports the FCC Canonical Data Model and serves as the reference implementation for the MVP.

FCC is implemented as an operational intelligence layer above CRM systems, planning tools, fundraising platforms, and knowledge repositories.

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

Task and project management systems remain the source of activity truth.

Examples:

* Planner
* Asana
* Smartsheet
* Microsoft Project

FCC does not replace task management systems.

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

Activities are consumed, not duplicated.

Activities remain in source systems.

FCC uses activity information to calculate:

* readiness
* follow-up compliance
* risk
* accountability
* workload indicators

---

## Principle 5

Power BI is the primary user experience.

SharePoint stores operational data.

Power Automate manages operational logic.

Power BI presents operational intelligence.

---

# Architectural Overview

```text
Source Systems
--------------------------------

CRM
(RE NXT, Salesforce)

Planning
(Planner, Asana, Smartsheet)

Knowledge
(SharePoint, Teams)

Finance
(Excel, ERP exports)

            ↓

Data Ingestion Layer

            ↓

FCC Operational Layer

            ↓

Rules & Intelligence Layer

            ↓

Power BI Command Centre

            ↓

Teams Notifications
AI Summaries
Management Reviews
```

---

# Microsoft 365 Components

## SharePoint

Purpose:

Operational data platform.

Stores:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Knowledge Metadata
* Metric Snapshots
* Configuration

---

## SharePoint Document Libraries

Purpose:

Store imported files and knowledge assets.

---

### Data Drop Library

Stores imported operational files.

Examples:

* RE NXT exports
* Planner exports
* Smartsheet exports
* Finance files
* External reference files

---

### Knowledge Library

Stores:

* SOPs
* Policies
* Playbooks
* Templates
* Post-Mortems
* Lessons Learned
* Decision Logs

---

## Power Automate

Purpose:

Transform source-system information into operational intelligence.

Responsibilities:

* file ingestion
* data validation
* readiness calculations
* commitment monitoring
* dependency monitoring
* risk generation
* snapshot creation
* notification delivery

---

## Power BI

Purpose:

Primary Command Centre experience.

Power BI provides:

* executive visibility
* operational management
* portfolio monitoring
* readiness monitoring
* risk management
* accountability reporting

Power BI is the primary FCC interface.

---

## Teams

Purpose:

Operational review and action.

Teams receives:

* alerts
* weekly digests
* escalation notices
* review packages

Teams supports management cadence rather than data storage.

---

# Operational Data Layer

FCC-owned records.

---

## Programs

Examples:

* Annual Giving
* Major Gifts
* Stewardship
* Events

---

## Initiatives

Examples:

* Spring Appeal
* Principal Gifts Portfolio
* Annual Gala
* Impact Reporting Cycle

---

## Commitments

Examples:

* Proposal Due
* Donor Follow-Up
* Campaign Launch Date
* Stewardship Report

---

## Dependencies

Examples:

* Finance Approval
* CEO Approval
* Legal Review
* Website Deployment

---

## Risks

Examples:

* Stalled Prospect
* Launch Delay
* Missing Approval
* Resource Constraint

---

## Knowledge Metadata

Stores document references.

Documents remain in SharePoint libraries.

---

## Metric Snapshots

Stores calculated historical metrics.

Examples:

* Readiness Score
* Follow-Up Compliance
* Open Risks
* Open Commitments

---

## Configuration

Stores:

* thresholds
* SLA definitions
* readiness weights
* escalation rules

---

# Source Activity Strategy

Activities are not FCC-owned objects.

Activities remain in source systems.

---

## Relationship Activities

Typical Sources:

* RE NXT Actions
* Salesforce Tasks

Examples:

* donor meeting
* qualification call
* stewardship visit
* proposal discussion

---

## Operational Activities

Typical Sources:

* Planner
* Asana
* Smartsheet
* Project

Examples:

* segmentation approval
* creative review
* venue booking
* website deployment

---

## FCC Usage

Activities may contribute to:

* readiness scoring
* commitment monitoring
* compliance monitoring
* risk generation

Activities are source data.

Not FCC-managed records.

---

# Data Ingestion Layer

## MVP Strategy

CSV-based ingestion.

Purpose:

Reduce complexity and implementation effort.

Supported Sources:

* RE NXT exports
* Planner exports
* Excel files
* Smartsheet exports

API integrations are not required for MVP.

---

# Rules & Intelligence Layer

The Rules Layer is the operational brain of FCC.

Rules transform source data into management intelligence.

---

## Examples

### Stalled Prospect

Rule:

No completed action within 90 days

Creates:

Risk

---

### Missing Next Action

Rule:

Active opportunity
AND
No future action

Creates:

Risk

---

### Overdue Commitment

Rule:

Due date passed
AND
Status not complete

Creates:

Alert

---

### Readiness Decline

Rule:

Readiness score below threshold

Creates:

Risk

---

# Power BI Architecture

Power BI consumes:

* SharePoint Lists
* Metric Snapshots
* Imported operational data

Power BI should not rely directly on raw CRM structures.

The semantic model is built around:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Metrics

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

Blocker and risk management.

---

## Commitments & Follow-Up

Accountability monitoring.

---

## Knowledgebase

Knowledge management and discovery.

---

# AI Architecture

AI receives:

* Metric Snapshots
* Risks
* Dependencies
* Commitments

AI does not calculate metrics.

AI provides:

* executive briefings
* readiness summaries
* risk summaries
* weekly digests

Power BI remains the calculation engine.

---

# Security & Governance

FCC minimizes donor PII.

Store:

* source system
* source record ID
* dates
* ownership
* statuses
* metrics

Avoid:

* donor notes
* personal contact information
* unnecessary sensitive information

CRM remains the donor system of record.

---

# MVP Scope

Included:

* SharePoint Lists
* SharePoint Libraries
* CSV ingestion
* RE NXT reference implementation
* Power Automate
* Power BI
* Teams integration
* AI summaries

Excluded:

* write-back to CRM
* API integrations
* SaaS platform
* Dataverse architecture
* predictive analytics

---

# Future Architecture

Potential future enhancements:

* RE NXT SKY API
* Salesforce APIs
* Planner APIs
* Dataverse
* Copilot Studio
* FCC SaaS Platform

These items are intentionally excluded from MVP.

---

# Success Criteria

The architecture succeeds when leadership can answer:

* What is at risk?
* What is overdue?
* What is blocked?
* What requires intervention?

within five minutes of opening the Executive Control Tower.

The architecture should support multiple fundraising disciplines without requiring separate systems for each team.
