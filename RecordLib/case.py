from __future__ import annotations
from dataclasses import asdict
from RecordLib.common import Charge, Person, Sentence
from typing import List
from datetime import date
import pytest
import logging
from dateutil.relativedelta import relativedelta

class Case:
    """
    Track information about a case

    """

    status: str
    county: str
    docket_number: str
    otn: str
    dc: str
    charges: List[Charge]
    fines_and_costs: int
    arrest_date: date
    disposition_date: date
    judge: str

    def __init__(
        self,
        status,
        county,
        docket_number,
        otn,
        dc,
        charges,
        fines_and_costs,
        arrest_date,
        disposition_date,
        judge,
    ) -> None:
        self.docket_number = docket_number
        self.otn = otn
        self.charges = charges
        self.fines_and_costs = fines_and_costs
        self.status = status
        self.county = county
        self.arrest_date = arrest_date
        self.disposition_date = disposition_date
        self.judge = judge
        self.dc = dc

    def years_passed_disposition(self) -> int:
        """ The number of years that have passed since the disposition date of this case."""
        try:
            return relativedelta(date.today(), self.disposition_date).years
        except:
            return 0

    def last_action(self) -> date:
        """
        The last arrest or disposition that happened in a case.

        Sometimes we want to know when the last thing in a case happened.

        If we can't find an arrest or disposition date, then Case#last_action will return a date far in the past. The theory is that if a case has no last action, then any expression asking "was the last action longer ago than X " should be True, so X needs to be basically infinitely far in the past.

        """
        try:
            return max(self.arrest_date, self.disposition_date)
        except TypeError:
            if self.arrest_date is None and self.disposition_date is not None:
                return self.disposition_date
            elif self.arrest_date is not None and self.disposition_date is None:
                return self.arrest_date
            else:
                logging.warning(f"Neither an arrest date nor a disposition date for {self.docket_number}. Returning datetime.min")
                return date.min

    def was_confined(self) -> bool:
        """
        True if there was a disposition that led to confinement.
        """
        if any(
            ["onfine" in s.sentence_type for c in self.charges for s in c.sentences]
        ):
            return True
        return False

    def end_of_confinement(self) -> date:
        """
        Try to figure out the days of confinement in a case.
        """
        if not self.was_confined():
            return None
        sentences = [s for c in self.charges for s in c.sentences]
        return max([s.sentence_date + s.sentence_length.max_time for s in sentences])

    def to_dict(self) -> dict:
        return {
            "docket_number": self.docket_number,
            "otn": self.otn,
            "charges": [asdict(c) for c in self.charges],
            "fines_and_costs": self.fines_and_costs,
            "status": self.status,
            "county": self.county,
            "arrest_date": self.arrest_date,
            "disposition_date": self.disposition_date,
            "judge": self.judge,
            "dc": self.dc
        }

    def partialcopy(self) -> Case:
        """
        Return a new Case that contains all the static info of this case, but no Charges.

        This method is used in rules a lot for building analyses of records.
        """
        return Case(
            docket_number = self.docket_number,
            otn = self.otn,
            charges = [],
            fines_and_costs = self.fines_and_costs,
            status = self.status,
            county = self.county,
            arrest_date = self.arrest_date,
            disposition_date = self.disposition_date,
            judge = self.judge,
            dc = self.dc
        )

    @staticmethod
    def order_cases_by_last_action(case):
        """
        Key for a sorted() call, to sort a list of cases by the last action date

        Args:
            case: a case

        Returns:
            The date of the last action on a case. Or, if there was no last action, today's date. This is so that cases that don't have a known last action

        Returns the date of the last action on a case
        """
        return case.last_action()
