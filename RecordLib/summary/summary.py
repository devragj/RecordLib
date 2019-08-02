from __future__ import annotations
from typing import List
from RecordLib.common import Person


class Summary:
    """
    Track information about a summary.
    """

    def __init__(self, defendant: Person = None, cases: List = None) -> None:
        self._defendant = defendant
        self._cases = cases

    def get_defendant(self) -> Person:
        return self._defendant

    def get_cases(self) -> List:
        return self._cases
