from __future__ import annotations
from dataclasses import asdict
from RecordLib.common import Charge, Sentence
from RecordLib.person import Person
from typing import List, Optional
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
    total_fines: int
    fines_paid: int
    complaint_date: date
    arrest_date: date
    disposition_date: date
    judge: str
    judge_address: str
    affiant: str
    arresting_agency: str
    arresting_agency_address: str

    @staticmethod
    def from_dict(dct: str) -> Optional[Case]:
        """Create a Case from a dict"""
        try:
            return Case(
                status = dct.get("status"),
                county = dct.get("county"),
                docket_number = dct["docket_number"], # if there's no docket_number at least, this should fail
                otn = dct.get("otn"),
                dc = dct.get("dc"),
                charges = [Charge.from_dict(c) for c in (dct.get("charges") or [])],
                total_fines = dct.get("total_fines"),
                fines_paid = dct.get("fines_paid"),
                complaint_date = dct.get("complaint_date"),
                arrest_date = dct.get("arrest_date"),
                disposition_date = dct.get("disposition_date"),
                judge = dct.get("judge"),
                judge_address = dct.get("judge_address"),
                affiant = dct.get("affiant"),
                arresting_agency = dct.get("arresting_agency"),
                arresting_agency_address = dct.get("arresting_agency_address"),
            )
        except:
            return None

    def __init__(
        self,
        status,
        county,
        docket_number,
        otn,
        dc,
        charges,
        total_fines = None,
        fines_paid = None,
        arrest_date = None,
        disposition_date = None,
        judge = None,
        judge_address = None,
        affiant = None,
        arresting_agency = None,
        arresting_agency_address = None,
        complaint_date = None,
    ) -> None:
        self.docket_number = docket_number
        self.otn = otn
        self.dc = dc
        self.charges = charges
        self.total_fines = total_fines
        self.fines_paid = fines_paid
        self.status = status
        self.county = county
        
        self.arrest_date = arrest_date
        self.complaint_date = complaint_date
        self.disposition_date = disposition_date

        self.judge = judge
        self.judge_address = judge_address
        self.affiant = affiant
        self.arresting_agency = arresting_agency
        self.arresting_agency_address = arresting_agency_address
        

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

    def partialcopy(self) -> Case:
        """
        Return a new Case that contains all the static info of this case, but no Charges.

        This method is used in rules a lot for building analyses of records.
        """
        return Case(
            docket_number = self.docket_number,
            otn = self.otn,
            charges = [],
            total_fines = self.total_fines,
            fines_paid = self.fines_paid,
            status = self.status,
            county = self.county,
            complaint_date = self.complaint_date,
            arrest_date = self.arrest_date,
            disposition_date = self.disposition_date,
            judge = self.judge,
            judge_address = self.judge_address,
            dc = self.dc,
            affiant = self.affiant,
            arresting_agency = self.arresting_agency,
            arresting_agency_address = self.arresting_agency_address,
        )

    def fines_remaining(self) -> Optional[int]:
        """ Return the value of the fines remaining on the case.

        Return None if the fines on the case aren't defined.
        """
        try:
            return self.total_fines - self.fines_paid
        except:
            return 0 if self.total_fines == 0 else None

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
