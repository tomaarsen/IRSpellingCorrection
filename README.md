# IRSpellingCorrection
Rule-based spelling correction as query pre-processing on IR systems

### Build the index
```
python -m pyserini.index -collection MsMarcoV2DocCollection \
                         -generator DefaultLuceneDocumentGenerator \
                         -input /path/to/msmarco_v2_doc \
                         -index indexes/lucene-index.msmarco-v2-doc \
                         -threads 12 \
                         -memorybuffer 512
```
where `/path/to/msmarco_v2_doc` is the path to the `msmarco_v2_doc` downloaded from the [2021 TREC Deep Learning Track](https://microsoft.github.io/msmarco/TREC-Deep-Learning-2021#document-ranking-dataset).

### Gathering the ranks
```
python -m pyserini.search
    --index data/indexes/lucene-index.msmarco-v2-doc
    --topics path/to/queries.tsv
    --output path/to/output/rank.txt
    --bm25
    --hits 10
    --batch-size 36
    --threads 12
```
where `path/to/queries.tsv` is the path to the `docv2_train_queries.tsv`, or some variation thereof, downloaded from the [2021 TREC Deep Learning Track](https://microsoft.github.io/msmarco/TREC-Deep-Learning-2021#document-ranking-dataset).

### Evaluating
#### Experiment 1
```
powershell ./tools/evaluate_ranks.ps1
```
#### Experiment 2
```
python ./tools/reduce.py
powershell ./tools/evaluate_relative_ranks.ps1
```

Experiment 1 and experiment 2 produces `data/output/ranking_eval.txt` and `data/output/ranking_relative_eval.txt`, respectively. As the files in `data/output` folder are too large, this folder was not uploaded to git. Instead, I copied these files over to [relative_eval.txt](ranking_eval.txt) and [relative_relative_eval.txt](relative_relative_eval.txt).

#### Authors
- Tom Aarsen
- Tijn Berns
- Daan Derks