Clear-Content -Path data/output/ranking_relative_eval.txt
$files = Get-ChildItem -Path data/output/reduced
foreach ($file in $files)
{
    "Rank for $($file.BaseName)" | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
    "Fixed scores:" | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
    python -m pyserini.eval.trec_eval -c -M 10 -m map -m ndcg data/output/reduced/$($file.BaseName)/qrels.txt ./data/output/reduced/$($file.BaseName)/fixed.txt | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
    python tools/trec_to_msmarco_run.py --input ./data/output/reduced/$($file.BaseName)/fixed.txt --output ./data/output/reduced/$($file.BaseName)/fixed_msmarco.txt --quiet
    python tools/msmarco_doc_eval.py --judgments ./data/output/reduced/$($file.BaseName)/qrels.txt --run ./data/output/reduced/$($file.BaseName)/fixed_msmarco.txt | Out-File -FilePath data/output/ranking_relative_eval.txt -Append

    "Original scores on the same queries:" | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
    python -m pyserini.eval.trec_eval -c -M 10 -m map -m ndcg data/output/reduced/$($file.BaseName)/qrels.txt ./data/output/reduced/$($file.BaseName)/original.txt | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
    python tools/trec_to_msmarco_run.py --input ./data/output/reduced/$($file.BaseName)/original.txt --output ./data/output/reduced/$($file.BaseName)/original_msmarco.txt --quiet
    python tools/msmarco_doc_eval.py --judgments ./data/output/reduced/$($file.BaseName)/qrels.txt --run ./data/output/reduced/$($file.BaseName)/original_msmarco.txt | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
    "=========================================" | Out-File -FilePath data/output/ranking_relative_eval.txt -Append
}