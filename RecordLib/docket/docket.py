from __future__ import annotations
from RecordLib.person import Person
from RecordLib.case import Case
from .parse_pdf import parse_pdf
from typing import Union, BinaryIO


class Docket:

    @staticmethod
    def from_pdf(pdf: Union[BinaryIO, str], tempdir: str = "tmp") -> Docket:
        """ Create a Docket from a pdf file. """
        # need to get (def, case), not just the Docket, b/c otherwise
        # there's a circular import, with Docket importing parse_pdf, and parse_pdf importing Docket
        defendant, case, errors = parse_pdf(pdf, tempdir=tempdir)
        return Docket(defendant, case), errors

    def __init__(self, defendant: Person, case: Case) -> None:
        self._defendant = defendant
        self._case = case