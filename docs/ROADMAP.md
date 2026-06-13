# ROADMAP.md

# Fundraising Command Centre (FCC)

## Product & Implementation Roadmap

Version: 1.0

---

# Purpose

This roadmap defines the sequence for designing, validating, prototyping, piloting, and eventually productizing the Fundraising Command Centre.

The roadmap prioritizes validation of the operating model before software development.

---

# Guiding Principle

The primary asset is not software.

The primary asset is the operational model.

The software implementation exists to support the operational model.

Therefore:

Operating model validation precedes technical implementation.

---

# Current Status

Completed:

✓ PROJECT_CONTEXT.md

✓ CANONICAL_DATA_MODEL.md

✓ CRM_MAPPING_WORKBOOK.md

✓ MS365_ARCHITECTURE.md

In Progress:

* Product design
* Canonical model refinement
* RE NXT mapping analysis

---

# Phase 1

## Canonical Model Validation

Goal:

Validate that the FCC model works across multiple fundraising disciplines.

Test against:

* Major Gifts
* Stewardship
* Direct Response
* Events
* Corporate Partnerships

Questions:

* Are Programs appropriate?
* Are Initiatives appropriate?
* Are Commitments appropriate?
* Are Dependencies appropriate?
* Are Risks appropriate?
* Are Knowledge assets appropriate?

Deliverable:

Validated Canonical Model.

Success Criteria:

Model works without major redesign.

---

# Phase 2

## RE NXT Mapping Prototype

Goal:

Test the canonical model against realistic RE NXT data.

Inputs:

* Synthetic RE NXT dataset
* Campaigns
* Appeals
* Gifts
* Pledges
* Opportunities
* Actions

Activities:

* Map Programs
* Map Initiatives
* Map Commitments
* Generate Risks
* Generate Metrics

Questions:

* Which mappings work?
* Which mappings fail?
* Which data quality issues emerge?

Deliverable:

Validated RE NXT Mapping Workbook.

Success Criteria:

Major Gifts and Stewardship scenarios work.

---

# Phase 3

## Microsoft 365 Foundation

Goal:

Build FCC operational layer.

Components:

* SharePoint Lists
* SharePoint Libraries
* Teams Structure

Build:

Programs

Initiatives

Commitments

Dependencies

Risks

Metric Snapshots

Configuration

Deliverable:

Working Microsoft 365 foundation.

Success Criteria:

Data can be loaded and viewed.

---

# Phase 4

## Data Ingestion

Goal:

Load source-system data into FCC.

Initial Strategy:

CSV only.

Sources:

* RE NXT exports
* Planner exports
* Excel files

Deliverable:

Data ingestion process.

Success Criteria:

Data refresh completed without manual manipulation.

---

# Phase 5

## Rules Engine

Goal:

Transform source data into operational intelligence.

Build Rules:

* Follow-up compliance
* Stalled prospects
* Commitment monitoring
* Dependency monitoring
* Readiness scoring
* Risk generation

Deliverable:

Operational rules library.

Success Criteria:

Risks and alerts generated automatically.

---

# Phase 6

## Power BI MVP

Goal:

Create first Command Centre dashboards.

Pages:

Executive Control Tower

Work Portfolio

Readiness & Execution

Dependencies & Risks

Commitments & Follow-Up

Knowledgebase

Deliverable:

Power BI prototype.

Success Criteria:

Executive users can identify priorities within five minutes.

---

# Phase 7

## Teams Operational Workflow

Goal:

Create operating cadence.

Build:

* Weekly review process
* Escalation process
* Alert notifications
* Leadership review package

Deliverable:

Operational governance process.

Success Criteria:

FCC becomes part of management rhythm.

---

# Phase 8

## AI Summaries

Goal:

Generate executive narratives from metrics.

Inputs:

* Metric Snapshots
* Risks
* Commitments
* Dependencies

Outputs:

* Weekly digest
* Executive briefing
* Readiness summary
* Risk summary

Principle:

AI explains.

AI does not calculate.

Deliverable:

AI-assisted management summaries.

Success Criteria:

Summaries save management review time.

---

# Phase 9

## Pilot Implementation

Goal:

Deploy FCC in a realistic environment.

Potential Pilot:

* RE NXT organization
* Microsoft 365 environment
* One fundraising team

Focus:

* Major Gifts
  OR
* Direct Response

Not both.

Deliverable:

Pilot implementation.

Success Criteria:

Operational value demonstrated.

---

# Phase 10

## Productization

Goal:

Create reusable implementation package.

Deliverables:

* Templates
* Documentation
* Deployment guides
* Mapping guides
* Rules library
* Power BI package

Success Criteria:

Implementation repeatable.

---

# Future Roadmap

Potential future enhancements:

* RE NXT API integration
* Salesforce integration
* Planner integration
* Dataverse architecture
* Copilot Studio agents
* FundraisingIQ SaaS platform

These items are explicitly out of scope for the initial MVP.

---

# Definition of Success

FCC succeeds when fundraising leadership can answer:

* What is at risk?
* What is overdue?
* What is blocked?
* What requires intervention?

within five minutes of opening the Command Centre.

