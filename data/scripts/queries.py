import parser
import csv


def fix_queries(queries, parsed_errors):
    with open(r"data/queries/fixed_queries.tsv", "w") as fixed_queries:
        for qid, query in queries:
            query = query.split()
            query = [parsed_errors.get(token, [token])[0] for token in query]
            fixed_queries.write(f"{qid}\t{' '.join(query)}\n")


if __name__ == "__main__":
    parsed_errors = parser.parse_all()

    with open(r"data/queries/docv2_train_queries.tsv") as f:
        queries = csv.reader(f, delimiter="\t")
        fix_queries(queries, parsed_errors)

    with open(r"data/queries/docv2_train_qrels.tsv") as f:
        qrels = csv.reader(f, delimiter="\t")

    # fix_queries(queries, parsed_errors)
