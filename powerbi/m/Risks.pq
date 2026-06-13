let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains risks.csv.
    SourceFile = SourceFolder & "/risks.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(EmptyToNull, {{"status", each if _ = null then null else Text.Proper(_), type nullable text}}),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"risk_id", each _, type nullable text},
            {"risk_name", each _, type nullable text},
            {"initiative", each _, type nullable text},
            {"risk_type", each _, type nullable text},
            {"severity", each _, type nullable text},
            {"likelihood", each _, type nullable text},
            {"status", each _, type nullable text},
            {"owner", each _, type nullable text},
            {"date_identified", each try Date.From(_) otherwise null, type nullable date},
            {"target_resolution_date", each try Date.From(_) otherwise null, type nullable date},
            {"source_system", each _, type nullable text},
            {"source_record_id", each _, type nullable text},
            {"mitigation_plan", each _, type nullable text}
        }
    )
in
    TypedColumns
