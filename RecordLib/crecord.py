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


class CRecord:
    """
    Track information about a criminal record
    """

    person: Person
    cases: List[Case]
    validator: cb.Validator

    def __init__(self, person: Person, cases: List[Case] = []):
        self.person = person
        self.cases = cases
        self.validate

    def to_dict(self) -> dict:
        return {"person": asdict(self.person),
                "cases": [c.to_dict() for c in self.cases]}

    def validate(self) -> bool:
        schema = yaml.load(open("CRecord.yml", "r"), Loader=yaml.SafeLoader)
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
        def_name = summary.get_defendant_name()
        self.person = Person(
            first_name=def_name.first_name,
            last_name=def_name.last_name
        )

        # Get the cases from the summary
        cases = summary.get_cases()

        return self
