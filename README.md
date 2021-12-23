# Effects of Query Correction Techniques on Ranking Systems
This repository contains the code used in our paper *Effects of Query Correction Techniques on Ranking Systems*, involving spelling correction as query pre-processing step of IR systems. We've included the abstract, alongside some of the commands we used to complete the experiments described in the paper. Note that we used Powershell scripts, and that this repository does not contain the index, TREC data, queries, qrels or rankings, as each of those files are either subject to a license or too big for git.

### Abstract
> To resolve misspellings in a query, this paper applies a dictionary lookup technique, a word modification technique and context-dependent word corrector. These techniques are used on data retrieved from the document ranking task of the 2021 version of the TREC Deep Learning Track. Two experiments are performed on the document ranking of a query, one to compare the different techniques and one to establish the performance gain or loss when applying a technique. One of the main findings of these experiments is that the techniques are trying to replace entities like names, locations and abbreviations to English words that the technique is aware of. This results in a loss of performance in the ranking.

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

### Authors
- Tom Aarsen
- Tijn Berns
- Daan Derks
