class AutoCorrectI:
    def __init__(self) -> None:
        pass

    def fix_query(self, query: str) -> str:
        raise NotImplementedError()


class Autocorrect(AutoCorrectI):
    def __init__(self) -> None:
        super().__init__()
        from autocorrect import Speller

        self.fix = Speller()

    def fix_query(self, query: str) -> str:
        return self.fix(query)


class NeuspellCorrecter(AutoCorrectI):
    def __init__(self) -> None:
        super().__init__()

    def fix_query(self, query: str) -> str:
        return self.checker.correct(query)


class BertsclstmCorrecter(NeuspellCorrecter):
    """BERT + SC-LSTM"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import BertsclstmChecker

        self.checker = BertsclstmChecker()
        self.checker.from_pretrained()


class CnnlstmCorrecter(NeuspellCorrecter):
    """CNN-LSTM"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import CnnlstmChecker

        self.checker = CnnlstmChecker()
        self.checker.from_pretrained()


class NestedlstmCorrecter(NeuspellCorrecter):
    """Nested-LSTM"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import NestedlstmChecker

        self.checker = NestedlstmChecker()
        self.checker.from_pretrained()


class SclstmCorrecter(NeuspellCorrecter):
    """SC-LSTM"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import SclstmChecker

        self.checker = SclstmChecker()
        self.checker.from_pretrained()


class SclstmbertCorrecter(NeuspellCorrecter):
    """SC-LSTM + BERT"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import SclstmbertChecker

        self.checker = SclstmbertChecker()
        self.checker.from_pretrained()


class BertCorrecter(NeuspellCorrecter):
    """BERT"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import BertChecker

        self.checker = BertChecker()
        self.checker.from_pretrained()


class SclstmelmoCorrecter(NeuspellCorrecter):
    """SC-LSTM + ELMO"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import SclstmelmoChecker

        self.checker = SclstmelmoChecker()
        self.checker.from_pretrained()


class ElmosclstmCorrecter(NeuspellCorrecter):
    """ELMO + SC-LSTM"""

    def __init__(self) -> None:
        super().__init__()
        from neuspell import ElmosclstmChecker

        self.checker = ElmosclstmChecker()
        self.checker.from_pretrained()


autocorrecters = [Autocorrect(), BertCorrecter()]

__all__ = [
    "AutoCorrectI",
    "Autocorrect",
    "autocorrecters",
    "NeuspellCorrecter",
    "BertsclstmCorrecter",
    "CnnlstmCorrecter",
    "NestedlstmCorrecter",
    "SclstmCorrecter",
    "SclstmbertCorrecter",
    "BertCorrecter",
    "SclstmelmoCorrecter",
    "ElmosclstmCorrecter",
]
