let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains dependencies.csv.
    SourceFile = SourceFolder & "/dependencies.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(EmptyToNull, {{"status", each if _ = null then null else Text.Proper(_), type nullable text}}),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"dependency_id", each _, type nullable text},
            {"dependency_name", each _, type nullable text},
            {"initiative", each _, type nullable text},
            {"dependency_type", each _, type nullable text},
            {"blocking_area", each _, type nullable text},
            {"impacted_area", each _, type nullable text},
            {"owner", each _, type nullable text},
            {"due_date", each try Date.From(_) otherwise null, type nullable date},
            {"status", each _, type nullable text},
            {"severity", each _, type nullable text},
            {"impact_description", each _, type nullable text},
            {"resolution_notes", each _, type nullable text}
        }
    )
in
    TypedColumns
