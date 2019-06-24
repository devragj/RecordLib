"""
Class that represents a Criminal Record in Pennsylvania.

Note - it looks like i can't use dataclasses throughout because
       dataclasses don't support nested dataclass without overriding init, so
       what's the point?
"""
from __future__ import annotations
import cerberus as cb  # type: ignore
import yaml
from typing import List
import pytest
from RecordLib.summary import Summary
from RecordLib.common import Case, Charge, Person
from dataclasses import asdict
from datetime import date
from dateutil.relativedelta import relativedelta

def years_since_last_arrested_or_prosecuted(crecord: CRecord) -> int:
    """
    How many years since a person was last arrested or prosecuted?
    """
    if len(crecord.cases) == 0: return None
    cases_ordered = sorted(crecord.cases, key=Case.order_cases_by_last_action)
    last_case = cases_ordered[-1]
    return relativedelta(last_case.last_action(), date.today()).years


def test_years_since_final_release(crecord: CRecord) -> int:
    """
    How many years since a person's final release from confinement or
    supervision?
    """
    pass

class CRecord:
    """
    Track information about a criminal record
    """

    person: Person
    cases: List[Case]
    validator: cb.Validator

    years_since_last_arrested_or_prosecuted = years_since_last_arrested_or_prosecuted


    def __init__(self, person: Person, cases: List[Case] = []):
        self.person = person
        self.cases = cases


    def to_dict(self) -> dict:
        return {
            "person": asdict(self.person),
            "cases": [c.to_dict() for c in self.cases],
        }

    def validate(self, crecord_schema: str = "CRecord.yml") -> bool:
        schema = yaml.load(open(crecord_schema, "r"), Loader=yaml.SafeLoader)
        self.validator = cb.Validator(schema)
        data = self.to_dict()
        if not self.validator.validate(data):
            return False
        return True

    def add_summary(self, summary: Summary) -> CRecord:
        """
        Add the information of a summary sheet to a CRecord.

        Args:
            summary (Summary): A parsed summary sheet.

        Returns:
            This updated CRecord object.
        """
        # Get D's name from the summary
        defendant = summary.get_defendant()
        self.person = Person(
            first_name=defendant.first_name, last_name=defendant.last_name,
            date_of_birth=defendant.date_of_birth
        )

        # Get the cases from the summary
        cases = summary.get_cases()

        return self
