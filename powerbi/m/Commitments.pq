let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains commitments.csv.
    SourceFile = SourceFolder & "/commitments.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(
        EmptyToNull,
        {{"status", each if _ = "Complete" then "Completed" else if _ = "In Progress" then "Open" else if _ = null then null else Text.Proper(_), type nullable text}}
    ),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"commitment_id", each _, type nullable text},
            {"commitment_name", each _, type nullable text},
            {"initiative", each _, type nullable text},
            {"commitment_type", each _, type nullable text},
            {"owner", each _, type nullable text},
            {"due_date", each try Date.From(_) otherwise null, type nullable date},
            {"status", each _, type nullable text},
            {"priority", each _, type nullable text},
            {"value_amount", each try Number.From(_) otherwise null, type nullable number},
            {"source_system", each _, type nullable text},
            {"source_record_id", each _, type nullable text},
            {"escalation_level", each _, type nullable text},
            {"notes", each _, type nullable text}
        }
    )
in
    TypedColumns
