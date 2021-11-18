import json
import re
from collections import defaultdict
from typing import DefaultDict, Dict, List, Set, Tuple

ASPELL = 1
HOLBROOK = 2
BIRKBECK = 4
WIKIPEDIA = 8


class Parser:
    """Parser class to read specific .dat files.
    Applies `pattern` iteratively on data from `filename`,
    and then calls `parse_corrects` and `parse_wrongs` on
    the "correct" and "wrong" groups that must be present
    in `pattern`. Fills out the mapping from misspellings
    to potential correct values.
    Designed to be overridden by subclasses.

    TODO: Handle "_" vs " " to represent spaces
    """

    def __init__(self, filename: str, pattern: re.Pattern):
        self.pattern = pattern
        self.filename = filename
        self.parsed = defaultdict(set)

    def add_misspelling(self, correct: str, wrong: str):
        """Fill out the mapping from misspelling (i.e. `wrong`)
        to the potential correction (i.e. `correct`)
        """
        self.parsed[wrong].add(correct)

    def parse_corrects(self, corrects: str) -> List[str]:
        """Return a list of correct words from the `corrects` string.
        Designed to be overridden by subclasses for specific parsers.
        """
        return [corrects]

    def parse_wrongs(self, wrongs: str) -> List[str]:
        """Return a list of misspelled words from the `wrongs` string.
        Designed to be overridden by subclasses for specific parsers.
        """
        return [wrongs]

    def parse(self) -> DefaultDict[str, Set[str]]:
        """Iteratively apply `self.pattern` on data from
        `self.filename`. Return a mapping from misspellings
        to potential corrections.

        :rtype: DefaultDict[str, Set[str]]
        """
        if self.parsed:
            return self.parsed

        with open(self.filename, "r", encoding="utf8") as f:
            for match in self.pattern.finditer(f.read()):
                corrects = self.parse_corrects(match.group("correct"))
                wrongs = self.parse_wrongs(match.group("wrong"))
                for correct in corrects:
                    for wrong in wrongs:
                        self.add_misspelling(correct, wrong)
        return self.parsed


class WikipediaParser(Parser):
    """Parser for Wikipedia misspelling data

    e.g:

        theyre->they're
        todays->today's
        wasnt->wasn't
    """

    def __init__(self, filename):
        pattern = re.compile(r"(?P<wrong>.*)->(?P<correct>[^\n]*)")
        super().__init__(filename, pattern)

    def parse_corrects(self, corrects: str) -> List[str]:
        return corrects.split(", ")


class DollarParser(Parser):
    """Parser for .dat data that uses $-notation,
    e.g. used by Birkbeck and Aspell.

    e.g:

        $Albert
        Ab
        $America
        Ameraca
        Amercia
        $American
        Ameracan
    """

    def __init__(self, filename):
        pattern = re.compile(r"\$(?P<correct>[^\n]*)\n(?P<wrong>[^\$]*)")
        super().__init__(filename, pattern)

    def parse_wrongs(self, wrongs: str) -> List[str]:
        return [wrong for wrong in wrongs.split("\n") if wrong]


class HolbrookParser(DollarParser):
    """Parser for .dat data that uses extended $-notation,
    with frequency of errors. E.g. used by Holbrook. The
    frequency is discarded.

    e.g:

        $Adam's
        Adam 1
        $After
        Artair 1
        $America
        American 1
    """

    def parse_corrects(self, corrects: str) -> List[str]:
        if corrects == "?":
            return []
        return [corrects]

    def parse_wrongs(self, wrongs: str) -> List[str]:
        return [
            " ".join(wrong.split(" ")[:-1]) for wrong in wrongs.split("\n") if wrong
        ]


WIKIPEDIA_PARSER = WikipediaParser("data/raw/wikipedia.dat")
BIRKBECK_PARSER = DollarParser("data/raw/birkbeck.dat")
HOLBROOK_PARSER = HolbrookParser("data/raw/holbrook.dat")
ASPELL_PARSER = DollarParser("data/raw/aspell.dat")


def merge(d1: DefaultDict[str, Set[str]], d2: DefaultDict[str, Set[str]]):
    """Merge values of `d2` into `d1`."""
    for key, value in d2.items():
        d1[key] |= value


def parse(
    data_flag: int, write: bool = False, verbose: bool = False
) -> Dict[str, Tuple[str]]:
    """Parse a set of the raw data, and optionally write to `processed/parsed.json`.

    :param data_flag: An integer indicating which datasets to use,
        e.g. `HOLBROOK + WIKIPEDIA` gives 10.
    :type data_flag: int
    :param write: Whether to write output to `processed/parsed.json`, defaults to False
    :type write: bool, optional
    :param verbose: Whether to print additional information. defaults to False
    :type verbose: bool, optional
    :return: The parsed data as a mapping from misspellings to a tuple of potential
        corrections.
    :rtype: Dict[str, Tuple[str]]
    """
    parsed_combined = defaultdict(set)

    if data_flag // WIKIPEDIA:
        merge(parsed_combined, WIKIPEDIA_PARSER.parse())
        if verbose:
            print(
                "Added Wikipedia data: "
                f"Corpus now contains {len(parsed_combined)} misspellings."
            )
        data_flag %= WIKIPEDIA

    if data_flag // BIRKBECK:
        merge(parsed_combined, BIRKBECK_PARSER.parse())
        if verbose:
            print(
                "Added Birkbeck data: "
                f"Corpus now contains {len(parsed_combined)} misspellings."
            )
        data_flag %= BIRKBECK

    if data_flag // HOLBROOK:
        merge(parsed_combined, HOLBROOK_PARSER.parse())
        if verbose:
            print(
                "Added Holbrook data: "
                f"Corpus now contains {len(parsed_combined)} misspellings."
            )
        data_flag %= HOLBROOK

    if data_flag // ASPELL:
        merge(parsed_combined, ASPELL_PARSER.parse())
        if verbose:
            print(
                "Added Aspell data: "
                f"Corpus now contains {len(parsed_combined)} misspellings."
            )
        data_flag %= ASPELL

    parsed_combined = {
        key: tuple(sorted(value)) for key, value in parsed_combined.items()
    }

    if write:
        with open(r"data/processed/parsed.json", "w", encoding="utf8") as f:
            json.dump(parsed_combined, f, indent=4)

    return parsed_combined


def parse_all(write: bool = False, verbose: bool = False) -> Dict[str, Tuple[str]]:
    """Parse all raw data, and optionally write to `processed/parsed.json`.

    :param write: Whether to write output to `processed/parsed.json`, defaults to False
    :type write: bool, optional
    :param verbose: Whether to print additional information. defaults to False
    :type verbose: bool, optional
    :return: The parsed data as a mapping from misspellings to a tuple of potential
        corrections.
    :rtype: Dict[str, Tuple[str]]
    """
    return parse(ASPELL + WIKIPEDIA + BIRKBECK + HOLBROOK, write=write, verbose=verbose)


def all_combinations():
    """Return a mapping of `data_flag` to `parse(data_flag)`,
    with all possible combinations of misspellings data.
    
    TODO: Consider an option to start at 0, for no misspellings.
    """
    return {i: parse(i, write=False, verbose=False) for i in range(1, 16)}


if __name__ == "__main__":
    parse_all(write=True, verbose=True)
    # output = all_combinations()
