let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains programs.csv.
    SourceFile = SourceFolder & "/programs.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(EmptyToNull, {{"status", each if _ = null then null else Text.Proper(_), type nullable text}}),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"program_id", each _, type nullable text},
            {"program_name", each _, type nullable text},
            {"program_type", each _, type nullable text},
            {"executive_owner", each _, type nullable text},
            {"department", each _, type nullable text},
            {"status", each _, type nullable text},
            {"strategic_goal", each _, type nullable text},
            {"start_date", each try Date.From(_) otherwise null, type nullable date},
            {"end_date", each try Date.From(_) otherwise null, type nullable date}
        }
    )
in
    TypedColumns
