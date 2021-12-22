
import glob
import os

with open("data/queries/docv2_train_queries.tsv", "r", encoding="utf8") as f:
    original_queries = f.readlines()

with open("data/output/0_rank.txt", "r", encoding="utf8") as f:
    original_rank = f.readlines()

os.makedirs("data/output/reduced", exist_ok=True)

for filename in glob.glob("data/queries/*_fixed_queries.tsv"):
    with open(filename, "r", encoding="utf8") as f:
        fixed_queries = f.readlines()
    
    # Gather the set of QID's for which _fixed_queries is different
    different = set()
    for original, fixed in zip(original_queries, fixed_queries):
        if original != fixed:
            orig_qid = original.split("\t")[0]
            fixed_qid = fixed.split("\t")[0]

            if orig_qid != fixed_qid:
                raise Exception(f"Different QID: {orig_qid} vs {fixed_qid}")
            
            different.add(orig_qid)
    
    # Create a copy of 0_rank.txt and *_rank.txt, containing only QID's in `different`
    prefix = os.path.basename(filename).split("_")[0]
    with open(f"data/output/{prefix}_rank.txt", "r", encoding="utf8") as f:
        fixed_rank = f.readlines()
    
    print(f"{prefix} modified {len(different)} queries out of {len(original_queries)} ({len(different) / len(original_queries) * 100:.2f}%).")

    os.makedirs(f"data/output/reduced/{prefix}", exist_ok=True)

    reduced_original_rank = [line for line in original_rank if line.split(" ")[0] in different]
    reduced_fixed_rank = [line for line in fixed_rank if line.split(" ")[0] in different]

    with open(f"data/output/reduced/{prefix}/original.txt", "w", encoding="utf8") as f:
        f.write("".join(reduced_original_rank))
    with open(f"data/output/reduced/{prefix}/fixed.txt", "w", encoding="utf8") as f:
        f.write("".join(reduced_fixed_rank))

    # Reduce qrels too
    with open(f"data/queries/docv2_train_qrels.tsv", "r", encoding="utf8") as f:
        qrels = f.readlines()

    shrunk_qrels = [
        qrel for qrel in qrels
        if qrel.split("\t")[0] in different
    ]

    with open(f"data/output/reduced/{prefix}/qrels.txt", "w", encoding="utf8") as f:
        f.write("".join(shrunk_qrels))