let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains configuration.csv.
    SourceFile = SourceFolder & "/configuration.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(EmptyToNull, {{"status", each if _ = null then null else Text.Proper(_), type nullable text}}),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"config_id", each _, type nullable text},
            {"config_area", each _, type nullable text},
            {"config_name", each _, type nullable text},
            {"config_value", each _, type nullable text},
            {"effective_date", each try Date.From(_) otherwise null, type nullable date},
            {"status", each _, type nullable text},
            {"notes", each _, type nullable text}
        }
    )
in
    TypedColumns
