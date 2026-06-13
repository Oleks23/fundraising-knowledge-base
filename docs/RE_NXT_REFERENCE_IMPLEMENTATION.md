# RE_NXT_REFERENCE_IMPLEMENTATION.md

# Fundraising Command Centre (FCC)

## RE NXT Reference Implementation

Version: 1.0

---

# Purpose

This document demonstrates how the Fundraising Command Centre (FCC) Canonical Data Model can be implemented using a typical Raiser's Edge NXT environment.

This document is a reference implementation only.

It is not intended to prescribe a single mapping approach for all RE NXT organizations.

Actual mappings must be documented and approved within CRM_MAPPING_WORKBOOK.md.

---

# Implementation Scenario

Organization Profile:

* Mid-sized Canadian charity
* RE NXT CRM
* Microsoft 365 environment
* Major Gifts team
* Stewardship team
* Direct Response team
* Annual Giving program
* Special Events program

Primary Goal:

Create a Command Centre that provides leadership visibility into:

* Readiness
* Commitments
* Dependencies
* Risks
* Follow-up compliance
* Operational performance

---

# RE NXT as System of Record

RE NXT remains the source of truth for:

* Constituents
* Gifts
* Pledges
* Opportunities
* Actions
* Campaigns
* Funds
* Appeals

FCC does not replace RE NXT.

FCC consumes selected operational data.

---

# Program Mapping

Programs represent the highest operational grouping level.

Programs are generally defined by fundraising leadership rather than directly imported from RE NXT.

Examples:

| Program                | Description                       |
| ---------------------- | --------------------------------- |
| Annual Giving          | Direct response fundraising       |
| Major Gifts            | Individual major gift fundraising |
| Stewardship            | Donor stewardship and reporting   |
| Events                 | Fundraising events                |
| Corporate Partnerships | Corporate fundraising             |

Programs are maintained within FCC.

Programs are not normally sourced directly from RE NXT.

---

# Initiative Mapping

Initiatives represent operational work portfolios.

## Direct Response Example

RE NXT:

Campaign:
FY2027 Annual Giving

Appeals:

* Spring Appeal
* Giving Tuesday
* Year-End Appeal

FCC:

Program:
Annual Giving

Initiatives:

* Spring Appeal
* Giving Tuesday
* Year-End Appeal

---

## Major Gifts Example

RE NXT:

Campaign:
Major Gifts FY2027

FCC:

Program:
Major Gifts

Initiatives:

* Principal Gifts Portfolio
* Leadership Gifts Portfolio
* Planned Giving Portfolio

These initiatives are operational constructs.

They may not exist directly in RE NXT.

---

## Stewardship Example

Program:

Stewardship

Initiatives:

* Impact Reporting Cycle
* Donor Recognition Program
* Foundation Reporting Program

---

# Activity Strategy

Activities remain in source systems.

FCC does not become the system of record for activities.

---

## Relationship Activities

Source:

RE NXT Actions

Examples:

* Qualification Call
* Donor Meeting
* Proposal Discussion
* Stewardship Visit
* Follow-Up Call

FCC consumes activity information to generate:

* Follow-up compliance metrics
* Commitment alerts
* Risk indicators

---

## Operational Activities

Source:

Planner
Asana
Smartsheet
Project

Examples:

* Segmentation Approval
* Creative Review
* Website Deployment
* Sponsorship Package Review

FCC consumes activity information for readiness and dependency monitoring.

---

# Commitment Mapping

Commitments are one of the most important FCC objects.

Commitments represent obligations.

Potential Sources:

* Opportunities
* Proposal Deadlines
* Stewardship Plans
* Reporting Requirements
* Campaign Milestones

---

## Example

RE NXT Opportunity

Title:
Smith Family Foundation

Ask Amount:
$250,000

Expected Ask Date:
2027-03-15

FCC Commitment:

Title:
Secure Smith Family Foundation Gift

Type:
Donor Commitment

Owner:
Assigned Gift Officer

Due Date:
2027-03-15

---

# Dependency Mapping

Dependencies are generally not stored in RE NXT.

Dependencies are created from:

* Planning tools
* Manual entry
* Readiness templates

Examples:

* CEO approval required
* Finance approval required
* Proposal review required

Dependencies are managed within FCC.

---

# Risk Mapping

Risks are primarily generated.

Examples:

---

## Stalled Prospect

Rule:

No completed action within 90 days

Create:

Risk

Type:
Pipeline Risk

---

## Missing Next Action

Rule:

Opportunity active

AND

No future action scheduled

Create:

Risk

Type:
Follow-Up Risk

---

## Overdue Proposal

Rule:

Proposal date passed

AND

Opportunity not closed

Create:

Risk

Type:
Commitment Risk

---

# Knowledge Mapping

Knowledge assets are maintained in Microsoft 365.

Examples:

* SOPs
* Gift Acceptance Policy
* Stewardship Standards
* Proposal Templates
* Campaign Playbooks
* Lessons Learned

Knowledge assets are generally not sourced from RE NXT.

---

# Metric Snapshot Examples

The following metrics are calculated periodically.

Major Gifts

* Active Opportunities
* Opportunity Value
* Pipeline Coverage
* Stalled Prospect Count
* Follow-Up Compliance
* Proposal Compliance

Stewardship

* Reports Due
* Reports Completed
* Stewardship Compliance

Direct Response

* Readiness Score
* Open Dependencies
* Launch Readiness

Events

* Sponsorship Progress
* Ticket Sales Progress
* Event Readiness

---

# Executive Control Tower Example

The Executive Control Tower may display:

Programs:
4

Initiatives:
12

Open Commitments:
37

Open Risks:
9

Critical Risks:
3

Follow-Up Compliance:
84%

Readiness Score:
78%

Dependencies Requiring Attention:
11

---

# Synthetic Data Strategy

The synthetic RE NXT dataset is used to validate:

* Mapping logic
* Power BI models
* Power Automate rules
* Risk generation
* Commitment monitoring

The synthetic dataset is not intended to fully represent operational activity management.

Additional operational data may be generated to simulate:

* Dependencies
* Risks
* Planner activities
* Readiness templates
* Knowledge assets

---

# Lessons Learned

The FCC implementation should not attempt to force RE NXT into the FCC Canonical Model.

Instead:

* RE NXT remains the fundraising system of record.
* FCC remains the operational intelligence platform.
* Mapping decisions are implementation-specific.
* Programs and Initiatives are management constructs.
* Commitments, Dependencies, Risks, and Knowledge are the primary FCC-managed objects.

This separation preserves the strengths of both platforms while providing leadership with a unified operational view.
