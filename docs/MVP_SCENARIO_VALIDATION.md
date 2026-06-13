# MVP_SCENARIO_VALIDATION.md

# Fundraising Command Centre

## MVP Scenario Validation

Version: 1.0

---

# Purpose

This document validates the FCC model against two different fundraising use cases:

1. Annual Giving / Direct Response
2. Major Gifts

The goal is to test whether the same model can support different fundraising disciplines without creating separate products.

---

# Scenario 1: Annual Giving

## Program

Annual Giving

## Initiative

Spring Appeal

## Operational Reality

The Spring Appeal is a direct response initiative requiring planning, segmentation, creative approval, finance coding, donation page setup, launch execution, and post-campaign review.

Most work is not managed in RE NXT.

Operational activities are likely managed in:

* Planner
* Asana
* Smartsheet
* Excel
* SharePoint

## Source Inputs

Possible inputs:

* RE NXT Campaign
* RE NXT Appeal
* Gift results
* Planner tasks
* Donation page checklist
* Finance coding approval
* Marketing production schedule

## FCC Objects

### Program

Annual Giving

### Initiative

Spring Appeal

### Commitments

* Campaign launch date
* Final segmentation approval
* Donation page test completion
* Finance designation approval
* Post-campaign review

### Dependencies

* Finance coding must be complete before donation page testing.
* Creative approval must be complete before email build.
* Segmentation must be approved before launch.
* Donation page must be tested before email launch.

### Risks

* Launch date at risk
* Finance approval delayed
* Segmentation incomplete
* Donation page not tested
* Campaign readiness below threshold

### Knowledge

* Direct Response Campaign Launch Playbook
* Email Approval SOP
* Donation Page Testing Checklist
* Post-Campaign Review Template

## Metrics

* Readiness Score
* Open Dependencies
* Overdue Commitments
* Launch Risk Level
* Knowledge Assets Due for Review
* Campaign Revenue vs Goal

---

# Scenario 2: Major Gifts

## Program

Major Gifts

## Initiative

Principal Gifts Portfolio

## Operational Reality

Major gift work is relationship-driven.

Most activities are managed in RE NXT through:

* Actions
* Opportunities
* Assigned solicitors
* Proposal records
* Constituent records

FCC should not replace RE NXT activity management.

FCC should monitor portfolio health, follow-up discipline, overdue commitments, stalled opportunities, and risks.

## Source Inputs

Possible inputs:

* RE NXT Opportunities
* RE NXT Actions
* RE NXT Constituents
* Solicitor assignments
* Proposal dates
* Ask amounts
* Opportunity stages
* Gift history

## FCC Objects

### Program

Major Gifts

### Initiative

Principal Gifts Portfolio

### Commitments

* Proposal due
* Donor follow-up due
* Stewardship visit due
* Ask strategy review
* Leadership briefing due

### Dependencies

* Prospect research required before solicitation.
* CEO briefing required before principal gift meeting.
* Proposal approval required before ask meeting.
* Stewardship report required before next solicitation.

### Risks

* Opportunity stalled
* No next action scheduled
* Proposal overdue
* High-value prospect inactive
* Portfolio overloaded
* Follow-up compliance below threshold

### Knowledge

* Major Gift Qualification SOP
* Proposal Approval Process
* Donor Briefing Template
* Principal Gift Strategy Playbook
* Stewardship Standards

## Metrics

* Active Opportunities
* Weighted Pipeline
* Stalled Prospects
* No Next Action Count
* Overdue Follow-Ups
* Proposal Compliance
* Portfolio Coverage
* Follow-Up Compliance

---

# Cross-Scenario Validation

The same FCC model supports both scenarios.

| FCC Object      | Annual Giving                     | Major Gifts                        |
| --------------- | --------------------------------- | ---------------------------------- |
| Program         | Annual Giving                     | Major Gifts                        |
| Initiative      | Spring Appeal                     | Principal Gifts Portfolio          |
| Commitment      | Launch deadline                   | Proposal / follow-up deadline      |
| Dependency      | Finance / creative / web approval | Research / CEO / proposal approval |
| Risk            | Launch readiness risk             | Pipeline / follow-up risk          |
| Knowledge       | Campaign playbooks                | Major gift SOPs                    |
| Metric Snapshot | Readiness / launch metrics        | Pipeline / follow-up metrics       |

---

# Key Finding

The model works because it does not force all teams into the same task-management structure.

Instead:

* Annual Giving activities remain in planning tools.
* Major Gifts activities remain in RE NXT.
* FCC monitors commitments, dependencies, risks, knowledge, and metrics across both.

---

# Design Implication

FCC should not create a universal Activities List in the MVP.

FCC should create:

* Programs
* Initiatives
* Commitments
* Dependencies
* Risks
* Knowledge
* Metric Snapshots
* Configuration

Activity data should remain in source systems and be imported or summarized only when needed.

---

# MVP Validation Result

The model appears viable for both:

* project-based fundraising work
* relationship-based fundraising work

Next validation scenarios:

* Stewardship
* Events
* Corporate Partnerships
