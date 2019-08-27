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
from RecordLib.summary import Summary
from RecordLib.common import Charge, Person
from RecordLib.case import Case
from dataclasses import asdict
from datetime import date
from dateutil.relativedelta import relativedelta
import logging

def years_since_last_arrested_or_prosecuted(crecord: CRecord) -> int:
    """
    How many years since a person was last arrested or prosecuted?

    If we can't tell how many years, return 0.
    """
    if len(crecord.cases) == 0:
        return float("-Inf")
    if any("Active" in case.status for case in crecord.cases):
        return 0
    cases_ordered = sorted(crecord.cases, key=Case.order_cases_by_last_action)
    last_case = cases_ordered[-1]
    try:
        return relativedelta(date.today(), last_case.last_action()).years
    except (ValueError, TypeError) as e:
        return 0


def years_since_final_release(crecord: CRecord) -> int:
    """
    How many years since a person's final release from confinement or
    supervision?

    If the record has no cases, the person was never confined, so return "infinity." If we cannot tell, because cases don't identify when confinement ended, return 0.
    """
    confinement_ends = [
        c.end_of_confinement() for c in crecord.cases if c.was_confined()
    ]
    if len(confinement_ends) == 0:
        return float("Inf")
    try:
        # nb. relativedelta(a, b) = c
        # if a is before b, then c is negative. if a is after b, c is positive.
        # relativedelta(today, yesterday) > 0
        # relativedelta(yesterday, today) < 0
        return max(relativedelta(date.today(),
                   max(confinement_ends)).years, 0)
    except (ValueError, TypeError):
        return 0


class CRecord:
    """
    Track information about a criminal record
    """

    person: Person
    cases: List[Case]
    validator: cb.Validator

    years_since_last_arrested_or_prosecuted = years_since_last_arrested_or_prosecuted

    years_since_final_release = years_since_final_release

    def __init__(self, person: Person = None, cases: List[Case] = None):
        self.person = person
        if cases is None:
            self.cases = list()
        else:
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

    def add_summary(self, summary: Summary, case_merge_strategy: str = "ignore_new", override_person: bool = False) -> CRecord:
        """
        Add the information of a summary sheet to a CRecord.

        Depending on the `case_merge_strategy`, any cases in the summary sheet
        that have a docket number that matches any case already in this
        CRecord will not be added, or the new case will overwrite the old.

        Depending on `override_person`, if a new Summary's Get Defendant returns a person who appears to be a different person, then the new Person will or will not be overwritten in this Record. If the CRecord has no person attribute, then the Person from the Summary will be added to this record regardless of this param.

        Args:
            summary (Summary): A parsed summary sheet.
            case_merge_strategy (str): "ignore_new" or "overwrite_old", which indicate whether duplicate new cases should be dropped or should replace the old ones

        Returns:
            This updated CRecord object.
        """
        # Get D's name from the summary
        if override_person or self.person is None:
            self.person = summary.get_defendant()
        # Get the cases from the summary
        docket_nums = [c.docket_number for c in self.cases]
        for i, new_case in enumerate(summary.get_cases()):
            if new_case.docket_number not in docket_nums:
                logging.info(f"Adding {new_case.docket_number} to record.")
                self.cases.append(new_case)
                docket_nums.append(new_case.docket_number)
            elif case_merge_strategy == "ignore_new":
                logging.info(f"Case with docket { new_case.docket_number } already part of record. Ignoring it.")
            elif case_merge_strategy == "overwrite_old":
                logging.info(f"Case with docket { new_case.docket_number } already part of record. Using it.")
                self.cases[i] = new_case
            else:
                logging.info(f"Case with docket { new_case.docket_number } already part of record, no merge strategy selected. Ignoring duplicate.")

        return self


    def add_docket(self: CRecord, docket: Docket) -> CRecord:
        """
        Add a docket to this criminal record and return the record.

        Args:
            docket (Docket): a Docket object, perhaps from a parsed pdf.

        Returns:
            This CRecord, with the information from `docket` incorporated into the record.
        """    
        replaced = False
        self.person = docket._defendant
        for i, case in enumerate(self.cases):
            if case.docket_number == docket._case.docket_number:
                replaced = True
                self.cases[i] = docket._case
        if replaced is False: self.cases.append(docket._case)
        return self
