"""
Common, simple dataclasses live here.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List
import functools
from datetime import date

@dataclass
class Person:
    """
    Track information about a person.
    """

    first_name: str
    last_name: str
    date_of_birth: date

    def age(self) -> int:
        """ Age in years """
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day))

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

    """

    status: str
    county: str
    docket_numbers: List[str]
    otn: str
    dc: str
    charges: List[Charge]
    fines_and_costs: int
    arrest_date: date
    disposition_date: date
    judge: str

    def __init__(
        self, status, county, docket_numbers, otn, dc, charges, fines_and_costs,
    arrest_date, disposition_date, judge) -> None:
        self.docket_numbers = docket_numbers
        self.otn = otn
        self.charges = charges
        self.fines_and_costs = fines_and_costs
        self.status = status
        self.county = county
        self.arrest_date = arrest_date
        self.disposition_date = disposition_date
        self.judge = judge

    def last_action(self) -> date:
        try:
            return max(self.arrest_date, self.disposition_date)
        except TypeError:
            if self.arrest_date is None and self.disposition_date is not None:
                return self.disposition_date
            elif self.arrest_date is not None and self.disposition_date is None:
                return self.arrest_date
            else:
                return None

    def to_dict(self) -> dict:
        return {
            "docket_numbers": self.docket_numbers,
            "otn": self.otn,
            "charges": [asdict(c) for c in self.charges],
            "fines_and_costs": self.fines_and_costs,
            "status": self.status,
            "county": self.county,
            "arrest_date": self.arrest_date,
            "disposition_date": self.disposition_date,
            "judge": self.judge
        }

    @staticmethod
    def order_cases_by_last_action(case):
        """ Key for a sorted() call, to sort a list of cases by the last action date"""
        return case.last_action()
