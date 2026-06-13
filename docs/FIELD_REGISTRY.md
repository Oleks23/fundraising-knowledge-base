# FIELD_REGISTRY.md

# Fundraising Command Centre (FCC)

## Field Registry — The Schema Contract

Version: 1.0

---

# Purpose

This document is the **single authoritative contract** for every field
in the FCC operational model. It exists to prevent the most expensive
class of bug in a multi-artifact build: the same concept spelled
differently across the SharePoint List, the CSV template, the Power
Query (M) script, and the DAX measure, producing artifacts that are
each locally correct but silently fail to connect.

Every generation prompt — SharePoint provisioning, CSV templates, the
synthetic data generator, Power Query, DAX — must reference this
registry for exact field names, types, and keys. No artifact may
introduce a field name not listed here. If a new field is needed, it
is added here first, then generated.

Where this registry and any other document disagree, **this registry
wins** for field-level naming and typing.

---

# How To Read This Registry

For each entity, the table lists every field with:

* **Field** — the canonical name. This exact string is the column
  name in CSV templates and the logical name basis in SharePoint.
* **Type** — SharePoint column type.
* **Req** — Required (Y) or Optional (O) at the data layer.
* **Key Role** — whether the field is a natural ID, a foreign key
  (lookup), a surrogate key (Power BI only), or a plain attribute.
* **Choice Values** — the locked option set, where applicable.
* **Touched By** — which artifacts read or write this field.

Artifact codes in "Touched By":

* **SP** — SharePoint List (provisioning)
* **CSV** — CSV import template
* **GEN** — synthetic data generator (Python)
* **M** — Power Query / M transformation
* **DAX** — Power BI measures / model
* **RULES** — Power Automate rules layer
* **AI** — AI summary inputs

---

# Global Conventions

1. **ID vs Key.** `<Entity> ID` is the natural/source identifier
   stored in SharePoint and CSVs (e.g. `Initiative ID`). `<Entity>
   Key` is a surrogate integer generated in Power Query for model
   relationships (e.g. `Initiative Key`). They are distinct and must
   never be conflated. Surrogate Keys are **Power BI only** — they do
   not appear in SharePoint or CSVs.

2. **Linking.** Child entities (Commitments, Dependencies, Risks,
   Knowledge, Metric Snapshots) link to **Initiative only**. The
   parent Program is always reached via Initiative → Program. No child
   entity stores a Program lookup.

3. **Status vocabulary.** Operational entities share a conformed
   status set. Knowledge uses a separate lifecycle set. Both are
   locked below and in POWER_BI_SEMANTIC_MODEL.md.

4. **"Overdue" is derived,** not stored — computed from Due Date and
   Status. It appears as a status value in reporting but is not a
   stored Choice option.

5. **Dates** are ISO 8601 (`YYYY-MM-DD`) in all CSVs and the generator.

6. **IDs** use the pattern `<PREFIX>-<zero-padded-int>`: PRG, INI, COM,
   DEP, RSK, KNW, SNP, CFG (e.g. `INI-0007`).

---

# Locked Choice Vocabularies

These option sets are fixed for v1 and referenced by name throughout
the tables below.

## Operational Status (Commitments, Dependencies, Risks)

| Value       | Applies To                   |
| ----------- | ---------------------------- |
| Open        | Commitment, Dependency, Risk |
| In Progress | Commitment                   |
| Completed   | Commitment                   |
| Resolved    | Dependency, Risk             |
| Monitoring  | Risk                         |

Derived (not stored): **Overdue** = Due Date < today AND Status not in
(Completed, Resolved).

## Knowledge Status

`Draft` · `Approved` · `Archived`

## Severity (Dependencies, Risks)

`Low` · `Medium` · `High`

## Likelihood (Risks)

`Low` · `Medium` · `High`

## Priority (Commitments)

`Low` · `Medium` · `High`

## Escalation Level (Commitments)

`None` · `Manager` · `Director`

## Initiative Stage (canonical pipeline taxonomy)

`Identify` · `Qualify` · `Cultivate` · `Solicit` · `Steward`

(Used where an Initiative or its source opportunities carry a pipeline
stage; locked from prior taxonomy decisions.)

## Source System

`RE NXT` · `Planner` · `Asana` · `Smartsheet` · `Excel` · `Manual` · `SharePoint`

## Readiness Band

`Red` · `Amber` · `Green`

## Readiness Module (weights live in Configuration)

`Prospect Coverage` (40%) · `Case for Support` (20%) · `Finance Setup`
(15%) · `Marketing Assets` (15%) · `Stewardship Plan` (10%)

Note: per-module score sourcing is deferred (see POWER_AUTOMATE_RULES.md).
The module names are locked; how each module's score is produced is not
yet designed. Do not add a per-record "Readiness Module" field to
operational entities to force this — it is not yet decided.

---

# 1. Programs

ID prefix: `PRG`

| Field           | Type                | Req | Key Role     | Choice Values        | Touched By              |
| --------------- | ------------------- | --- | ------------ | -------------------- | ----------------------- |
| Program ID      | Single line text    | Y   | Natural ID   | —                    | SP, CSV, GEN, M, DAX    |
| Program Name    | Single line text    | Y   | Attribute    | —                    | SP, CSV, GEN, M, DAX, AI |
| Program Type    | Choice              | Y   | Attribute    | (client-defined)     | SP, CSV, GEN, M, DAX    |
| Executive Owner | Person              | O   | Attribute    | —                    | SP, CSV, GEN, M, DAX    |
| Department      | Choice              | Y   | Attribute    | (client-defined)     | SP, CSV, GEN, M, DAX    |
| Status          | Choice              | Y   | Attribute    | Active, Inactive     | SP, CSV, GEN, M, DAX    |
| Strategic Goal  | Multiple lines text | O   | Attribute    | —                    | SP, CSV                 |
| Start Date      | Date                | O   | Attribute    | —                    | SP, CSV, GEN, M, DAX    |
| End Date        | Date                | O   | Attribute    | —                    | SP, CSV, GEN, M, DAX    |
| Program Key     | (surrogate)         | —   | Surrogate    | —                    | M, DAX                  |

---

# 2. Initiatives

ID prefix: `INI`

| Field            | Type                | Req | Key Role          | Choice Values                              | Touched By               |
| ---------------- | ------------------- | --- | ----------------- | ------------------------------------------ | ------------------------ |
| Initiative ID    | Single line text    | Y   | Natural ID        | —                                          | SP, CSV, GEN, M, DAX     |
| Initiative Name  | Single line text    | Y   | Attribute         | —                                          | SP, CSV, GEN, M, DAX, AI |
| Program          | Lookup to Programs  | Y   | FK → Program ID   | —                                          | SP, CSV, GEN, M, DAX     |
| Initiative Type  | Choice              | Y   | Attribute         | Portfolio, Appeal, Event, Program Cycle    | SP, CSV, GEN, M, DAX     |
| Owner            | Person              | Y   | Attribute         | —                                          | SP, CSV, GEN, M, DAX     |
| Department       | Choice              | Y   | Attribute         | (client-defined)                           | SP, CSV, GEN, M, DAX     |
| Status           | Choice              | Y   | Attribute         | Active, Complete, On Hold                  | SP, CSV, GEN, M, DAX     |
| Start Date       | Date                | O   | Attribute         | —                                          | SP, CSV, GEN, M, DAX     |
| Target Date      | Date                | Y   | Attribute         | —                                          | SP, CSV, GEN, M, DAX     |
| Goal Amount      | Currency            | O   | Attribute         | —                                          | SP, CSV, GEN, M, DAX     |
| Readiness Score  | Number              | O   | Attribute (calc)  | 0–100                                      | SP, GEN, M, DAX, RULES   |
| Risk Score       | Number              | O   | Attribute (calc)  | 0–100                                      | SP, GEN, M, DAX, RULES   |
| Source System    | Choice              | O   | Attribute         | Source System vocab                        | SP, CSV, GEN, M          |
| Source Record ID | Single line text    | O   | Attribute         | —                                          | SP, CSV, GEN, M          |
| Initiative Key   | (surrogate)         | —   | Surrogate         | —                                          | M, DAX                   |
| Program Key      | (surrogate)         | —   | FK (surrogate)    | —                                          | M, DAX                   |

Note: `Program` (the lookup) carries Program ID at the data layer; the
`Program Key` surrogate is added in Power Query for the snowflake join.

---

# 3. Commitments

ID prefix: `COM` · Links to Initiative only

| Field            | Type                  | Req | Key Role           | Choice Values        | Touched By                    |
| ---------------- | --------------------- | --- | ------------------ | -------------------- | ----------------------------- |
| Commitment ID    | Single line text      | Y   | Natural ID         | —                    | SP, CSV, GEN, M, DAX          |
| Commitment Name  | Single line text      | Y   | Attribute          | —                    | SP, CSV, GEN, M, DAX, AI      |
| Initiative       | Lookup to Initiatives | Y   | FK → Initiative ID | —                    | SP, CSV, GEN, M, DAX          |
| Commitment Type  | Choice                | Y   | Attribute (→ dim)  | Donor Follow-Up, Proposal, Stewardship, Operational, Vendor | SP, CSV, GEN, M, DAX |
| Owner            | Person                | Y   | Attribute          | —                    | SP, CSV, GEN, M, DAX          |
| Due Date         | Date                  | Y   | Attribute          | —                    | SP, CSV, GEN, M, DAX, RULES   |
| Status           | Choice                | Y   | Attribute          | Operational Status   | SP, CSV, GEN, M, DAX, RULES   |
| Priority         | Choice                | O   | Attribute          | Priority             | SP, CSV, GEN, M, DAX          |
| Value Amount     | Currency              | O   | Attribute          | —                    | SP, CSV, GEN, M, DAX          |
| Escalation Level | Choice                | O   | Attribute          | Escalation Level     | SP, CSV, GEN, M, RULES        |
| Source System    | Choice                | O   | Attribute          | Source System vocab  | SP, CSV, GEN, M               |
| Source Record ID | Single line text      | O   | Attribute          | —                    | SP, CSV, GEN, M               |
| Notes            | Multiple lines text   | O   | Attribute          | —                    | SP, CSV                       |
| Initiative Key   | (surrogate)           | —   | FK (surrogate)     | —                    | M, DAX                        |

---

# 4. Dependencies

ID prefix: `DEP` · Links to Initiative only · Carries BOTH Type and Areas

| Field              | Type                  | Req | Key Role           | Choice Values                          | Touched By                  |
| ------------------ | --------------------- | --- | ------------------ | -------------------------------------- | --------------------------- |
| Dependency ID      | Single line text      | Y   | Natural ID         | —                                      | SP, CSV, GEN, M, DAX        |
| Dependency Name    | Single line text      | Y   | Attribute          | —                                      | SP, CSV, GEN, M, DAX, AI    |
| Initiative         | Lookup to Initiatives | Y   | FK → Initiative ID | —                                      | SP, CSV, GEN, M, DAX        |
| Dependency Type    | Choice                | Y   | Attribute (→ dim)  | Approval, Resource, Technology, Vendor, Review | SP, CSV, GEN, M, DAX |
| Blocking Area      | Choice                | Y   | Attribute          | (client-defined depts/functions)      | SP, CSV, GEN, M, DAX        |
| Impacted Area      | Choice                | Y   | Attribute          | (client-defined depts/functions)      | SP, CSV, GEN, M, DAX        |
| Owner              | Person                | Y   | Attribute          | —                                      | SP, CSV, GEN, M, DAX        |
| Due Date           | Date                  | Y   | Attribute          | —                                      | SP, CSV, GEN, M, DAX, RULES |
| Status             | Choice                | Y   | Attribute          | Open, Resolved                         | SP, CSV, GEN, M, DAX, RULES |
| Severity           | Choice                | Y   | Attribute          | Severity                               | SP, CSV, GEN, M, DAX, RULES |
| Impact Description  | Multiple lines text   | O   | Attribute          | —                                      | SP, CSV, GEN, AI            |
| Resolution Notes   | Multiple lines text   | O   | Attribute          | —                                      | SP, CSV                     |
| Initiative Key     | (surrogate)           | —   | FK (surrogate)     | —                                      | M, DAX                      |

---

# 5. Risks

ID prefix: `RSK` · Links to Initiative only · May be rules-generated

| Field                  | Type                  | Req | Key Role           | Choice Values                              | Touched By                  |
| ---------------------- | --------------------- | --- | ------------------ | ------------------------------------------ | --------------------------- |
| Risk ID                | Single line text      | Y   | Natural ID         | —                                          | SP, CSV, GEN, M, DAX, RULES |
| Risk Name              | Single line text      | Y   | Attribute          | —                                          | SP, CSV, GEN, M, DAX, AI    |
| Initiative             | Lookup to Initiatives | Y   | FK → Initiative ID | —                                          | SP, CSV, GEN, M, DAX        |
| Risk Type              | Choice                | Y   | Attribute (→ dim)  | Pipeline, Operational, Data Quality, Staffing, Readiness, Commitment, Follow-Up, Dependency, Governance | SP, CSV, GEN, M, DAX, RULES |
| Severity               | Choice                | Y   | Attribute          | Severity                                   | SP, CSV, GEN, M, DAX, RULES |
| Likelihood             | Choice                | Y   | Attribute          | Likelihood                                 | SP, CSV, GEN, M, DAX        |
| Status                 | Choice                | Y   | Attribute          | Open, Monitoring, Resolved                 | SP, CSV, GEN, M, DAX, RULES |
| Owner                  | Person                | O   | Attribute          | —                                          | SP, CSV, GEN, M, DAX        |
| Date Identified        | Date                  | Y   | Attribute          | —                                          | SP, CSV, GEN, M, DAX, RULES |
| Target Resolution Date | Date                  | O   | Attribute          | —                                          | SP, CSV, GEN, M, DAX        |
| Source                 | Choice                | O   | Attribute          | Manual, Rule                               | SP, CSV, GEN, M, RULES      |
| Source Record ID       | Single line text      | O   | Attribute          | —                                          | SP, CSV, GEN, M             |
| Mitigation Plan        | Multiple lines text   | O   | Attribute          | —                                          | SP, CSV, AI                 |
| Initiative Key         | (surrogate)           | —   | FK (surrogate)     | —                                          | M, DAX                      |

Note: Risk Type spans the canonical categories plus the rule-generated
types (Commitment, Follow-Up, Dependency, Governance) emitted by
POWER_AUTOMATE_RULES.md. All are valid members of Dim Risk Type.

---

# 6. Knowledge

ID prefix: `KNW` · Initiative link OPTIONAL (org-wide assets allowed)

| Field            | Type                     | Req | Key Role           | Choice Values                        | Touched By               |
| ---------------- | ------------------------ | --- | ------------------ | ------------------------------------ | ------------------------ |
| Knowledge ID     | Single line text         | Y   | Natural ID         | —                                    | SP, CSV, GEN, M, DAX     |
| Title            | Single line text         | Y   | Attribute          | —                                    | SP, CSV, GEN, M, DAX, AI |
| Knowledge Type   | Choice                   | Y   | Attribute          | SOP, Policy, Playbook, Template, Post-Mortem, Decision Log | SP, CSV, GEN, M, DAX |
| Initiative       | Lookup to Initiatives    | O   | FK → Initiative ID | — (blank = org-wide)                 | SP, CSV, GEN, M, DAX     |
| Owner            | Person                   | O   | Attribute          | —                                    | SP, CSV, GEN, M, DAX     |
| Status           | Choice                   | Y   | Attribute          | Knowledge Status                     | SP, CSV, GEN, M, DAX     |
| Source Authority | Choice                   | Y   | Attribute          | Working, Approved, Official          | SP, CSV, GEN, M, DAX     |
| Review Date      | Date                     | O   | Attribute          | —                                    | SP, CSV, GEN, M, DAX, RULES |
| Document Link    | Hyperlink                | O   | Attribute          | —                                    | SP, CSV                  |
| Tags             | Managed metadata or text | O   | Attribute          | —                                    | SP, CSV                  |
| Initiative Key   | (surrogate)              | —   | FK (surrogate)     | —                                    | M, DAX                   |

Note: Knowledge uses Dim Knowledge Status, not the shared operational
Dim Status. Source Authority (Working/Approved/Official) is distinct
from Status (Draft/Approved/Archived); both exist. "Approved" appears
in both vocabularies with different meaning — Status.Approved is a
lifecycle state, Source Authority.Approved is a credibility level.

---

# 7. Metric Snapshots

ID prefix: `SNP` · Initiative link OPTIONAL (blank = Program/org level)

| Field            | Type                  | Req | Key Role           | Choice Values        | Touched By                   |
| ---------------- | --------------------- | --- | ------------------ | -------------------- | ---------------------------- |
| Snapshot ID      | Single line text      | Y   | Natural ID         | —                    | SP, CSV, GEN, M, DAX         |
| Snapshot Date    | Date                  | Y   | Attribute          | —                    | SP, CSV, GEN, M, DAX, AI     |
| Initiative       | Lookup to Initiatives | O   | FK → Initiative ID | — (blank = org-wide) | SP, CSV, GEN, M, DAX         |
| Metric Name      | Choice or text        | Y   | Attribute          | (metric catalog)     | SP, CSV, GEN, M, DAX, AI     |
| Metric Value     | Number                | Y   | Attribute          | —                    | SP, CSV, GEN, M, DAX, AI     |
| Metric Unit      | Choice                | O   | Attribute          | Percent, Count, Currency, Score | SP, CSV, GEN, M, DAX |
| Threshold Status | Choice                | O   | Attribute          | Readiness Band       | SP, CSV, GEN, M, DAX, AI     |
| Source           | Choice                | O   | Attribute          | Source System vocab  | SP, CSV, GEN, M              |
| Notes            | Multiple lines text   | O   | Attribute          | —                    | SP, CSV                      |
| Initiative Key   | (surrogate)           | —   | FK (surrogate)     | —                    | M, DAX                       |

Metric Name catalog (locked v1): `Readiness Score`, `Follow-Up
Compliance`, `Commitment Compliance`, `Pipeline Coverage`, `Open Risks`,
`Critical Risks`, `Open Commitments`, `Overdue Commitments`, `Open
Dependencies`, `Stalled Prospect Count`, `Dependency Count`.

---

# 8. Configuration

ID prefix: `CFG` · No Initiative link (global settings)

| Field          | Type                | Req | Key Role     | Choice Values                                                    | Touched By        |
| -------------- | ------------------- | --- | ------------ | --------------------------------------------------------------- | ----------------- |
| Config ID      | Single line text    | Y   | Natural ID   | —                                                               | SP, CSV, GEN      |
| Config Area    | Choice              | Y   | Attribute    | Readiness Weights, SLA Thresholds, Risk Thresholds, Escalation Rules, Departments | SP, CSV, GEN, RULES |
| Config Name    | Single line text    | Y   | Attribute    | —                                                               | SP, CSV, GEN, RULES |
| Config Value   | Single line text    | Y   | Attribute    | —                                                               | SP, CSV, GEN, RULES |
| Effective Date | Date                | O   | Attribute    | —                                                               | SP, CSV, GEN      |
| Status         | Choice              | Y   | Attribute    | Active, Inactive                                                | SP, CSV, GEN, RULES |
| Notes          | Multiple lines text | O   | Attribute    | —                                                               | SP, CSV           |

Required Configuration seed rows (the readiness weights, per the
module decision):

| Config Area       | Config Name        | Config Value |
| ----------------- | ------------------ | ------------ |
| Readiness Weights | Prospect Coverage  | 40           |
| Readiness Weights | Case for Support   | 20           |
| Readiness Weights | Finance Setup      | 15           |
| Readiness Weights | Marketing Assets   | 15           |
| Readiness Weights | Stewardship Plan   | 10           |

---

# Derived / Model-Only Dimensions

These are NOT SharePoint Lists. They are built in Power Query and exist
only in the semantic model. The generator does not emit CSVs for them.

| Dimension          | Built From                                   | Touched By |
| ------------------ | -------------------------------------------- | ---------- |
| Dim Date           | Generated date table                         | M, DAX     |
| Dim Owner          | Distinct Owner across facts + Person fields  | M, DAX     |
| Dim Department     | Distinct Department values                   | M, DAX     |
| Dim Status         | Conformed operational status set             | M, DAX     |
| Dim Knowledge Status | Knowledge lifecycle set                    | M, DAX     |
| Dim Commitment Type | Distinct Commitment Type values             | M, DAX     |
| Dim Risk Type      | Distinct Risk Type values                    | M, DAX     |
| Dim Dependency Type | Distinct Dependency Type values             | M, DAX     |

---

# Change Control

This registry is versioned. Any field addition, rename, type change,
or choice-set change is made HERE FIRST, the version is bumped, and
only then are the affected artifacts regenerated. A field that exists
in an artifact but not in this registry is a defect in the artifact,
not a gap in the registry.
