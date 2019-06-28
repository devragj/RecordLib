from dataclasses import asdict
from RecordLib.common import Charge, Person, Sentence
from typing import List
from datetime import date


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
        TODO try to figure out the days of confinement in a case.
        """
        if not self.was_confined():
            return None
        sentences = [s for c in self.charges for s in c.sentences]
        return max([s.sentence_date for s in sentences])

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
        }

    @staticmethod
    def order_cases_by_last_action(case):
        """ Key for a sorted() call, to sort a list of cases by the last action date"""
        return case.last_action()
