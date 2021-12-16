Clear-Content -Path data/output/ranking_eval.txt
for ($i = 0; $i -lt 16; $i++)
{
    "Rank $i" | Out-File -FilePath data/output/ranking_eval.txt -Append
    python -m pyserini.eval.trec_eval -c -M 10 -m map -m ndcg data/queries/docv2_train_qrels.tsv data/output/$($i)_rank.txt | Out-File -FilePath data/output/ranking_eval.txt -Append
    python .\trec_to_msmarco_run.py --input .\data\output\$($i)_rank.txt --output .\data\output\msmarco\$($i)_rank.txt --quiet
    python msmarco_doc_eval.py --judgments .\data\queries\docv2_train_qrels.tsv --run .\data\output\msmarco\$($i)_rank.txt | Out-File -FilePath data/output/ranking_eval.txt -Append
}