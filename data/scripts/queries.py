import csv
from typing import Dict, List, Tuple

from .parser import all_combinations


def fix_queries(data_flag: int, queries: List[str], parsed_errors: Dict[str, Tuple[str]]):
    """Update `queries` according to `parsed_errors` misspellings

    :param data_flag: The data flag as used in the parser.
        e.g. `HOLBROOK + WIKIPEDIA` gives 10.
    :type data_flag: int
    :param queries: List of query strings, starting with a query ID.
    :type queries: List[str]
    :param parsed_errors: Dictionary of typo to tuple of potential fixes.
    :type parsed_errors: Dict[str, Tuple[str]]
    """
    with open(rf"data/queries/{data_flag}_fixed_queries.tsv", "w", encoding="utf8") as fixed_queries:
        for qid, query in queries:
            query = query.split()
            query = [parsed_errors.get(token, [token])[0] for token in query]
            fixed_queries.write(f"{qid}\t{' '.join(query)}\n")


if __name__ == "__main__":
    with open(r"data/queries/docv2_train_queries.tsv", "r", encoding="utf8") as f:
        queries = csv.reader(f, delimiter="\t")
        parsed_errors_dict = all_combinations()
        for data_flag, parsed_errors in parsed_errors_dict.items():
            fix_queries(data_flag, queries, parsed_errors)

