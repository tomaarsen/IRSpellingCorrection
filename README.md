# IRSpellingCorrection
Rule-based spelling correction as query pre-processing on IR systems

The command used for getting the results is of the form:
```
python -m pyserini.search
    --index data/indexes/lucene-index.msmarco-v2-doc
    --topics data/queries/6_fixed_queries.tsv
    --output data/output/6_rank.txt
    --bm25
    --hits 10
    --batch-size 36
    --threads 12
```
This is the example used for `data/output/6_rank.txt`.