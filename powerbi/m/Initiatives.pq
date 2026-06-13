let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains initiatives.csv.
    SourceFile = SourceFolder & "/initiatives.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(
        EmptyToNull,
        {{"status", each if _ = "Completed" then "Complete" else if _ = null then null else Text.Proper(_), type nullable text}}
    ),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"initiative_id", each _, type nullable text},
            {"initiative_name", each _, type nullable text},
            {"program", each _, type nullable text},
            {"initiative_type", each _, type nullable text},
            {"owner", each _, type nullable text},
            {"department", each _, type nullable text},
            {"status", each _, type nullable text},
            {"start_date", each try Date.From(_) otherwise null, type nullable date},
            {"target_date", each try Date.From(_) otherwise null, type nullable date},
            {"goal_amount", each try Number.From(_) otherwise null, type nullable number},
            {"readiness_score", each try Number.From(_) otherwise null, type nullable number},
            {"risk_score", each try Number.From(_) otherwise null, type nullable number},
            {"source_system", each _, type nullable text},
            {"source_record_id", each _, type nullable text}
        }
    )
in
    TypedColumns
