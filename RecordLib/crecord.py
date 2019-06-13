"""
Class that represents a Criminal Record in Pennsylvania.

Note - it looks like i can't use dataclasses throughout because
       dataclasses don't support nested dataclass without overriding init, so
       what's the point?
"""
import cerberus as cb # type: ignore
from dataclasses import dataclass
import yaml
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

    docket_number: str
    otn: str
    charges: List[Charge]
    fines_and_costs: int

    def __init__(self, data):
        self.docket_number = data["docket_number"]
        self.otn = data["otn"]
        self.charges = [Charge(c) for c in data["charges"]]
        self.fines_and_costs = data["fines_and_costs"]


class CRecord:
    """
    Track information about a criminal record
    """

    person: Person
    cases: List[Case]
    validator: cb.Validator

    def __init__(self, data=None):
        if data is not None:
            schema = yaml.load(open("CRecord.yml", "r"), Loader=yaml.SafeLoader)
            self.validator = cb.Validator(schema)
            if not self.validator.validate(data):
                raise AssertionError

            self.person = Person(**data["person"])
            if "cases" in data:
                self.cases = [Case(c) for c in data["cases"]]
            else:
                self.cases = []
