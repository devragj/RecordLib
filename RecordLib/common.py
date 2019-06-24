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
