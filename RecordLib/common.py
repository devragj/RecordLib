"""
Common, simple dataclasses live here.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
import functools


@dataclass
class Person:
    """
    Track information about a person.
    """

    first_name: str
    last_name: str


@dataclass
class Charge:
    """
    Track information about a charge
    """

    offense: str
    grade: str
    statute: str
    disposition: str



class Case:
    """
    Track information about a case

    A Case is uniquely identified by its OTN, the "Offense Tracking Number."
    A case _usually_ also only has one docket number. One situation in which a case has multiple docket numbers is when a case starts in one county
    and then is transferred to a new county.
    """

    status: str
    county: str
    docket_numbers: List[str]
    otn: str
    dc: str
    charges: List[Charge]
    fines_and_costs: int

    def __init__(self, status, county, docket_numbers, otn, dc, charges, fines_and_costs) -> None:
        self.docket_numbers = docket_numbers
        self.otn = otn
        self.charges = charges
        self.fines_and_costs = fines_and_costs
        self.status = status
        self.county = county




class CaseList:

    cases: List[Case]

    @staticmethod
    def merge(case1: Case, case2: Case) -> Case:
        """
        Combine two cases with the same otn

        """
        if case1.otn != case2.otn:
            raise ValueError("OTNs not the same for these cases.")
        return Case(

        )


    def __init__(self) -> None:
        self._cases = []

    def __len__(self) -> int:
        """ Return the length of this list of cases."""
        return len(self._cases)

    def add(self, case: Case) -> CaseList:
        """ Add a case to the list, or combine if there's already a case with
        the same otn

        N.B. This method won't detect if a case gets added directly to _cases."""
        for i, c in enumerate(self._cases):
            if case.otn == c.otn:
                self._cases[i] = CaseList.merge(self._cases[i], case)
                return self
        self._cases.append(case)
        return self
