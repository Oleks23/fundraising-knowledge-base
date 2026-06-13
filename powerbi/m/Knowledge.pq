let
    // SourceFolder is a Power BI text parameter pointing to the folder that contains knowledge.csv.
    SourceFile = SourceFolder & "/knowledge.csv",
    Source = Csv.Document(File.Contents(SourceFile), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, List.Transform(Table.ColumnNames(PromotedHeaders), (columnName) => {columnName, each if _ is text then Text.Trim(_) else _, type text})),
    EmptyToNull = Table.ReplaceValue(TrimmedText, "", null, Replacer.ReplaceValue, Table.ColumnNames(TrimmedText)),
    NormalizedStatus = Table.TransformColumns(EmptyToNull, {{"status", each if _ = null then null else Text.Proper(_), type nullable text}}),
    TypedColumns = Table.TransformColumns(
        NormalizedStatus,
        {
            {"knowledge_id", each _, type nullable text},
            {"title", each _, type nullable text},
            {"knowledge_type", each _, type nullable text},
            {"initiative", each _, type nullable text},
            {"owner", each _, type nullable text},
            {"status", each _, type nullable text},
            {"source_authority", each _, type nullable text},
            {"review_date", each try Date.From(_) otherwise null, type nullable date},
            {"document_link", each _, type nullable text},
            {"tags", each _, type nullable text}
        }
    )
in
    TypedColumns
