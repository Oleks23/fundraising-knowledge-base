# Power Query M Scripts

These scripts define the Sprint 2 Power BI data layer for the Fundraising Command Centre Microsoft 365 MVP.

Each query loads one FCC-owned CSV file from `data/sample/` by using a Power BI text parameter named `SourceFolder`. Set `SourceFolder` to the folder that contains the sample CSV files, for example a local checkout path ending in `data/sample`.

No Activities query is included. Activities remain in source systems such as RE NXT Actions, Salesforce Tasks, Planner, Asana, Smartsheet, or Microsoft Project. FCC may consume activity-derived commitments, risks, and metric snapshots, but it does not create an Activities table.

## Query Map

| Query | CSV source | FCC object | Key columns |
| --- | --- | --- | --- |
| `Programs.pq` | `programs.csv` | Program | `program_id`, `program_name`, `status` |
| `Initiatives.pq` | `initiatives.csv` | Initiative | `initiative_id`, `program`, `status`, `source_system`, `source_record_id` |
| `Commitments.pq` | `commitments.csv` | Commitment | `commitment_id`, `initiative`, `due_date`, `status`, `source_system`, `source_record_id` |
| `Dependencies.pq` | `dependencies.csv` | Dependency | `dependency_id`, `initiative`, `due_date`, `status`, `severity` |
| `Risks.pq` | `risks.csv` | Risk | `risk_id`, `initiative`, `severity`, `likelihood`, `status`, `source_system`, `source_record_id` |
| `Knowledge.pq` | `knowledge.csv` | Knowledge | `knowledge_id`, `initiative`, `status`, `review_date` |
| `MetricSnapshots.pq` | `metric_snapshots.csv` | Metric Snapshot | `snapshot_id`, `snapshot_date`, `initiative`, `metric_name`, `source_system` |
| `Configuration.pq` | `configuration.csv` | Configuration | `config_id`, `config_area`, `config_name`, `status` |

## Data Layer Behavior

The queries:

- load CSV files from `SourceFolder`
- promote headers
- trim text values
- convert blank strings to null
- apply date and numeric types
- normalize known status aliases where needed
- preserve `source_system` and `source_record_id`

## Relationship Expectations

The expected model path is:

```text
Programs
  -> Initiatives
      -> Commitments
      -> Dependencies
      -> Risks
      -> Knowledge
      -> Metric Snapshots
```

Child records carry an Initiative reference only. Program-level reporting should flow through `Initiatives.program` rather than direct Program fields on child tables.

## Known MVP Limitations

- These queries load from CSV files only; live SharePoint, CRM, or API connectors are outside this Sprint 2 scope.
- The scripts do not create derived dimensions, surrogate keys, DAX measures, or report visuals.
- Type dimensions such as Commitment Type, Risk Type, and Dependency Type should be created later as reference queries from these base tables.
- Readiness and compliance placeholders are loaded as metric snapshots when present, but no readiness or compliance formula is created here.
- Person fields are loaded as text display names for MVP purposes; identity resolution is deferred.
- Knowledge document links are loaded as text URLs, not SharePoint document objects.
