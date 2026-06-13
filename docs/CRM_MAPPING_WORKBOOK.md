# CRM_MAPPING_WORKBOOK.md

# Fundraising Command Centre

## CRM Mapping Workbook

Version 2.0

---

# Purpose

This workbook documents how a client's operational reality is translated into the FCC Canonical Data Model.

The purpose is not to map CRM objects directly.

The purpose is to identify:

* Programs
* Initiatives
* Dependencies
* Commitments
* Risks
* Knowledge

that the organization needs to manage.

CRM data is one source of information used to build that model.

---

# Mapping Methodology

## Step 1

Understand how the organization works.

Not:

"What objects exist?"

Instead:

"What work is being managed?"

---

## Step 2

Identify Programs.

Examples:

* Annual Giving
* Major Gifts
* Events
* Corporate Partnerships
* Stewardship
* Capital Campaign

Programs become the highest operational layer.

---

## Step 3

Identify Initiatives.

Examples:

Annual Giving

* Spring Appeal
* Giving Tuesday
* Year-End Appeal

Events

* Annual Gala
* Golf Tournament

Major Gifts

* Principal Gifts Portfolio
* Leadership Gifts Portfolio

Stewardship

* Foundation Reporting Program
* Impact Reporting Cycle

---

## Step 4

Identify Activities.

Examples:

* Approve segmentation
* Prepare proposal
* Conduct donor meeting
* Finalize sponsorship package
* Review impact report

---

## Step 5

Identify Commitments.

Examples:

* Proposal due
* Donor follow-up
* Stewardship report
* Sponsor benefit delivery
* Campaign launch date

---

## Step 6

Identify Dependencies.

Examples:

* Finance approval
* Legal review
* Website deployment
* Prospect research

---

## Step 7

Identify Risks.

Examples:

* Stalled prospects
* Missing readiness items
* Data quality issues
* Delayed approvals

---

# Program Mapping

Document how source-system objects contribute to Programs.

Programs are usually not sourced from a single CRM object.

Example:

Program

Annual Giving

Source Inputs

* Campaigns
* Appeals
* Funds
* Budget Structure

---

# Initiative Mapping

Document how Initiatives are identified.

Examples:

Annual Giving

Source

Appeals

Examples

* Spring Appeal
* Year-End Appeal

Events

Source

Events Calendar

Examples

* Annual Gala
* Golf Tournament

Major Gifts

Source

Portfolio Structure

Examples

* Principal Gifts
* Leadership Gifts

---

# Source Activity Assessment

Activities are not treated as FCC-owned core objects.

Activities usually remain in their source systems, such as:

- RE NXT Actions
- Salesforce Tasks
- Planner Tasks
- Asana Tasks
- Smartsheet Tasks
- Microsoft Project tasks

FCC consumes activity data to evaluate execution, follow-up discipline, readiness, dependencies, and risk.

## Activity Types

### Relationship Activities

Examples:

- Donor meeting
- Qualification call
- Proposal discussion
- Stewardship visit
- Follow-up call

Typical sources:

- RE NXT Actions
- Salesforce Tasks

### Operational Activities

Examples:

- Approve segmentation
- Confirm finance coding
- Finalize creative
- Test donation page
- Secure venue
- Approve sponsorship package

Typical sources:

- Planner
- Asana
- Smartsheet
- Microsoft Project
- Excel

## Assessment Questions

- Which systems currently manage activities?
- Are activities consistently recorded?
- Are due dates reliable?
- Are owners reliable?
- Are completed dates reliable?
- Are activity statuses reliable?
- Can activities be linked to a Program or Initiative?
- Can activities be used for follow-up compliance?
- Can activities be used for readiness scoring?
- Can activities be used to generate risks?
- What activity data should remain read-only?
- What activity data should be summarized into FCC metrics?

## Mapping Guidance

Activities should not normally be recreated as FCC-owned records.

Instead:

- Relationship activities remain in CRM.
- Operational activities remain in planning tools.
- FCC imports or references activity data.
- FCC creates metrics, alerts, risks, and summaries from activity data.

## Example

RE NXT Action:

- Action Type: Call
- Constituent: Donor A
- Assigned Solicitor: Sarah Mitchell
- Due Date: 2026-07-15
- Status: Not Completed

FCC interpretation:

- Source Activity
- Used for follow-up compliance
- May generate an overdue commitment alert
- May contribute to a stalled prospect risk

# Commitment Mapping

Document operational obligations.

Potential Sources

* Opportunities
* Proposals
* Stewardship Plans
* Event Deliverables
* Vendor Agreements

Important:

An Opportunity is not automatically a Commitment.

Implementation review required.

---

# Activity Mapping

Potential Sources

* Actions
* Tasks
* Planner
* Asana
* Smartsheet
* Manual Entry

Activity quality assessment required.

---

# Dependency Mapping

Potential Sources

* Planner
* Project Plans
* Readiness Checklists
* Manual Entry

Dependencies are usually derived.

Dependencies rarely exist in CRM.

---

# Risk Mapping

Potential Sources

* Operational Rules
* Readiness Scores
* Missing Activities
* Missing Commitments
* Data Quality Checks

Risks are typically generated.

Risks are rarely imported.

---

# Knowledge Mapping

Potential Sources

* SharePoint
* Teams
* SOP Libraries
* Policies
* Playbooks

Knowledge is usually managed entirely within Microsoft 365.

---

# RE NXT Assessment

## Campaign Usage

Document:

* How campaigns are used
* Whether campaigns represent Programs
* Whether campaigns represent Initiatives

---

## Appeal Usage

Document:

* Appeal hierarchy
* Appeal reporting
* Appeal ownership

Potential Initiative candidates.

---

## Opportunity Usage

Document:

* Ask management process
* Proposal process
* Stage definitions
* Forecasting process

Potential Commitment candidates.

---

## Action Usage

Document:

* Action discipline
* Next-action compliance
* Activity logging standards

Potential Activity candidates.

---

## Portfolio Usage

Document:

* Portfolio ownership
* Assignment rules
* Portfolio review process

Potential Initiative candidates.

---

# Data Quality Assessment

Assess:

* Completeness
* Consistency
* Timeliness
* Reliability

before any mapping decisions are approved.

---

# Approval

Mappings must be approved before:

* SharePoint List design
* Power Automate design
* Power BI semantic model design
* AI summary configuration

Approved By:

---

Date:

---

