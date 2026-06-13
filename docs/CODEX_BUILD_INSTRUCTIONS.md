# CODEX_BUILD_INSTRUCTIONS.md

# Fundraising Command Centre (FCC)

## Codex Build Instructions

Version: 1.0

---

# Purpose

This document defines how Codex should participate in the development of the Fundraising Command Centre (FCC).

Codex is primarily an implementation tool.

Architecture decisions originate from repository documentation.

Codex should not redefine the architecture.

---

# Required Reading Order

Before generating code, documentation, or implementation assets, read:

1. PROJECT_CONTEXT.md
2. CANONICAL_DATA_MODEL.md
3. CRM_MAPPING_WORKBOOK.md
4. MS365_ARCHITECTURE.md
5. SHAREPOINT_LISTS_DESIGN.md
6. POWER_BI_SEMANTIC_MODEL.md
7. POWER_AUTOMATE_RULES.md
8. ROADMAP.md
9. RE_NXT_REFERENCE_IMPLEMENTATION.md
10. MVP_SCENARIO_VALIDATION.md

These documents represent the authoritative architecture.

---

# FCC Design Principles

FCC is:

* an operational intelligence platform
* a management platform
* a readiness platform
* a risk management platform

FCC is not:

* a CRM
* a project management tool
* a marketing platform

---

# Canonical Objects

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

Do not create a universal FCC Activities table unless explicitly instructed.

---

# Source Systems

Typical source systems:

CRM

* RE NXT
* Salesforce

Planning

* Planner
* Asana
* Smartsheet

Knowledge

* SharePoint
* Teams

Finance

* Excel exports

---

# MVP Architecture

Microsoft 365 implementation.

Core Components:

* SharePoint Lists
* SharePoint Libraries
* Power Automate
* Power BI
* Teams

Initial integrations use CSV files.

Do not assume API integration.

---

# Development Priorities

Priority 1

Build operational foundation.

Priority 2

Build reporting.

Priority 3

Build automation.

Priority 4

Build AI summaries.

---

# Expected Artifact Types

Codex should prioritize creation of:

* Python
* Power Query (M)
* DAX
* JSON
* CSV templates
* SharePoint provisioning assets
* Power Automate specifications
* Power BI documentation

Avoid generating excessive architecture documentation.

Architecture already exists.

---

# Sprint 1

## Foundation Assets

Generate:

### SharePoint Assets

* List schemas
* Column definitions
* Lookup relationships

Possible outputs:

```text
sharepoint/
```

### CSV Templates

Generate templates for:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Metric Snapshots

Possible outputs:

```text
data/templates/
```

### Synthetic FCC Data

Extend:

```text
scripts/generate_renxt_data_v4.py
```

Generate:

* commitments.csv
* dependencies.csv
* risks.csv
* initiatives.csv
* metric_snapshots.csv

Possible outputs:

```text
scripts/
```

---

# Sprint 2

## Data Layer

Generate:

### Power Query

Create M scripts for:

* RE NXT Opportunities
* RE NXT Actions
* Planner Exports
* Risk Generation Inputs

Possible outputs:

```text
powerbi/m/
```

---

### Data Model Documentation

Create:

* table relationships
* surrogate keys
* dimensional structures

Possible outputs:

```text
powerbi/model/
```

---

# Sprint 3

## Power BI

Generate:

### DAX Measures

Examples:

* Readiness Score
* Follow-Up Compliance
* Commitment Compliance
* Open Risk Count
* Dependency Count

Possible outputs:

```text
powerbi/dax/
```

---

### Report Metadata

Generate:

* KPI definitions
* visual specifications
* page documentation

Possible outputs:

```text
powerbi/pages/
```

---

# Sprint 4

## Automation

Generate Power Automate implementation specifications.

Flows:

* Import RE NXT Data
* Import Planning Data
* Commitment Monitoring
* Dependency Monitoring
* Risk Generation
* Snapshot Creation
* Teams Notifications

Possible outputs:

```text
flows/
```

---

# Sprint 5

## AI Summaries

Generate:

* Weekly Digest Prompts
* Executive Briefing Prompts
* Readiness Summary Prompts
* Risk Narrative Prompts

AI consumes:

* Metric Snapshots
* Risks
* Dependencies
* Commitments

AI should not calculate metrics.

---

# Coding Standards

Generated assets should:

* be modular
* be documented
* use configuration tables
* avoid hard-coded thresholds
* support future multi-client deployment

---

# Mapping Standards

Do not assume:

```text
Opportunity = Commitment
Campaign = Program
Appeal = Initiative
```

Mappings are implementation-specific.

Always refer to:

CRM_MAPPING_WORKBOOK.md

before generating transformations.

---

# Validation Requirements

Before generating implementation assets:

Validate against:

* Annual Giving Scenario
* Major Gifts Scenario

Artifacts should support both.

---

# Definition of Success

Codex succeeds when it produces implementation assets that:

* align with FCC architecture
* support Microsoft 365 deployment
* support RE NXT reference implementation
* avoid duplication of CRM and planning systems
* accelerate MVP development

without redesigning the Canonical Model.
