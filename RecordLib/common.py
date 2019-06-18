"""
Common, simple dataclasses live here.
"""
from dataclasses import dataclass
from typing import List

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
    disposition: str


class Case:
    """
    Track information about a case
    """

    status: str
    county: str
    docket_number: str
    otn: str
    charges: List[Charge]
    fines_and_costs: int

    def __init__(self, data):
        self.docket_number = data.get("docket_number")
        self.otn = data.get("otn")
        self.charges = [Charge(c) for c in data["charges"]]
        self.fines_and_costs = data.get("fines_and_costs")
        self.status = data.get("status")
        self.county = data.get("county")
