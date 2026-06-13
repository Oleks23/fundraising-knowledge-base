# PROJECT_CONTEXT.md

# Fundraising Command Centre (FCC)

## Project Overview

Fundraising Command Centre (FCC) is a Microsoft 365-based fundraising operations system designed to provide executive visibility, operational accountability, campaign readiness monitoring, follow-up discipline, dependency management, and AI-assisted operational intelligence.

FCC is not a CRM.

FCC is not a project management system.

FCC is not a reporting platform.

FCC sits above these systems and provides a unified operational view of fundraising execution.

---

# Vision

Most nonprofits have:

* CRM systems
* Online giving platforms
* Marketing platforms
* Project management tools
* Finance systems
* Microsoft 365
* Reporting tools

However, they lack a system that answers:

* Are we on track?
* What is at risk?
* What needs attention today?
* What is blocking success?
* What should leadership focus on this week?

FCC is designed to answer those questions.

---

# Product Philosophy

CRM manages donors.

Project management manages tasks.

Power BI manages reporting.

FCC manages execution.

---

# Initial Platform Strategy

Version 1 is Microsoft 365 based.

Primary components:

* SharePoint Lists
* SharePoint Document Libraries
* Power Automate
* Power BI
* Microsoft Teams
* Azure OpenAI (optional)

FCC is implemented inside the client's Microsoft 365 tenant.

No standalone SaaS platform will be developed during Phase 1.

---

# Universal Work Model

All fundraising disciplines map into the same operational model.

## Core Objects

### Initiative

A fundraising work portfolio.

Examples:

* Annual Appeal
* Capital Campaign
* Major Gifts Portfolio
* Gala Event
* Stewardship Program
* Monthly Giving Program

### Activity

Work required to advance an initiative.

Examples:

* Prospect qualification
* Create sponsorship package
* Secure venue
* Draft proposal
* Approve segmentation

### Dependency

A relationship where one activity cannot proceed until another activity, decision, deliverable, or approval is completed.

Examples:

* Finance approval
* Legal review
* Website update
* Prospect research completion

### Commitment

An obligation that must be fulfilled.

Examples:

* Donor follow-up
* Stewardship report
* Proposal deadline
* Sponsor benefit delivery
* Campaign launch date

### Risk

Anything that may prevent successful execution.

Examples:

* Missing approvals
* Stalled prospects
* Incomplete readiness items
* Data quality issues
* Resource constraints

### Knowledge

Institutional knowledge required to support operations.

Examples:

* SOPs
* Playbooks
* Policies
* Templates
* Decision logs
* Post-mortems
* Lessons learned

---

# Core User Interfaces

## Executive Control Tower

Provides leadership visibility into:

* Readiness
* Risks
* Commitments
* Dependencies
* Forecasts
* Follow-up compliance

## Work Portfolio

Provides team-specific operational views.

Examples:

* Appeals
* Events
* Major Gifts
* Stewardship

## Readiness & Execution

Tracks readiness items and execution status.

## Dependencies & Risks

Tracks blockers and operational risks.

## Commitments & Follow-Up

Tracks accountability and obligation completion.

## Knowledgebase

Provides operational knowledge and AI-assisted retrieval.

---

# Microsoft 365 Architecture

## SharePoint Lists

Primary operational store.

Planned Lists:

* Initiatives
* Activities
* Dependencies
* Commitments
* Risks
* Knowledge
* Metric Snapshots
* Configuration

## SharePoint Document Library

Stores imported CRM extracts.

Examples:

* RE NXT exports
* Salesforce exports
* Planning tool exports

## Power Automate

Provides:

* Readiness scoring
* SLA monitoring
* Alert generation
* Snapshot creation
* Data validation

## Power BI

Provides:

* Executive dashboards
* Operational dashboards
* Trend reporting
* Risk reporting
* Readiness reporting

## Teams

Provides:

* Weekly operational reviews
* Alert delivery
* Executive digests
* Team collaboration

---

# CRM Strategy

FCC does not replace CRM systems.

CRM remains the source of donor truth.

Initial target CRM:

* Raiser's Edge NXT

Future support:

* Salesforce Nonprofit Cloud
* Salesforce NPSP
* DonorPerfect
* Keela

---

# Source System Mapping Layer

A mapping layer translates source-system objects into the FCC Canonical Model.

Example:

RE NXT Opportunity
→ Commitment

RE NXT Action
→ Activity

RE NXT Portfolio Assignment
→ Initiative

RE NXT Pledge
→ Commitment

RE NXT Stalled Opportunity
→ Risk

Planner Task
→ Activity

Blocked Planner Task
→ Dependency

SharePoint SOP
→ Knowledge

The canonical model is stable.

CRM mappings are implementation-specific.

No source-system object has a guaranteed one-to-one relationship with a canonical object.
---

# Data Principles

FCC minimizes donor PII.

Store:

* Source system
* Source record ID
* Assigned fundraiser
* Stage
* Dates
* Metrics
* Operational status

Avoid:

* Detailed donor notes
* Contact information
* Sensitive financial information

---

# AI Principles

AI assists with interpretation.

AI does not calculate metrics.

AI does not become the source of truth.

AI receives precomputed metrics and operational summaries.

Outputs:

* Weekly digest
* Executive briefing
* Risk narrative
* Readiness summary
* Board-report content

---

# Current MVP Scope

Phase 1:

* SharePoint Lists
* CSV ingestion
* RE NXT mapping
* Power Automate rules
* Power BI dashboards
* Teams review process
* AI executive summaries

Excluded:

* Live CRM write-back
* Full SaaS platform
* Multi-CRM support
* Copilot Studio implementation
* Advanced predictive modeling

---

# Success Criteria

The platform succeeds when leadership can answer:

* What is at risk?
* What is overdue?
* What is blocked?
* What needs attention this week?

within five minutes of opening the Command Centre.

---

# Repository Structure

/docs
PROJECT_CONTEXT.md
CANONICAL_DATA_MODEL.md
CRM_MAPPING_WORKBOOK.md
MS365_ARCHITECTURE.md
ROADMAP.md

/data
/scripts
/powerbi
/flows

PROJECT_CONTEXT.md is the authoritative source document that all future architecture, coding, Power BI, Power Automate, and AI work must reference.
