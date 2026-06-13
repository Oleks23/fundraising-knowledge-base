let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains metric_snapshots.csv.
    SourceFile = SourceFolder & "/metric_snapshots.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    TypedColumns = Table.TransformColumns(
        EmptyToNull,
        {
            {"snapshot_id", each _, type nullable text},
            {"snapshot_date", each try Date.From(_) otherwise null, type nullable date},
            {"initiative", each _, type nullable text},
            {"metric_name", each _, type nullable text},
            {"metric_value", each try Number.From(_) otherwise null, type nullable number},
            {"metric_unit", each _, type nullable text},
            {"threshold_status", each _, type nullable text},
            {"source_system", each _, type nullable text},
            {"notes", each _, type nullable text}
        }
    )
in
    TypedColumns
