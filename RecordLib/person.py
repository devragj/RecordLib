from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from datetime import date
from dateutil.relativedelta import relativedelta
from RecordLib.common import Address


@dataclass
class Person:
    """
    Track information about a person.
    """

    first_name: str
    last_name: str
    date_of_birth: date
    aliases: List[str] = None
    date_of_death: Optional[date] = None
    ssn: Optional[str] = None
    address: Optional[Address] = None

    @staticmethod
    def from_dict(dct: dict) -> Person:
        """ Create a Person from a dict describing one. """
        if dct is not None:
            return Person(
                first_name = dct.get("first_name"),
                last_name = dct.get("last_name"),
                date_of_birth = dct.get("date_of_birth"), 
                date_of_death = dct.get("date_of_death"),
                aliases = dct.get("aliases") or [],
                ssn = dct.get("ssn"),
                address = Address.from_dict(dct.get("address"))
            )

    def age(self) -> int:
        """ Age in years """
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def years_dead(self) -> float:
        """Return number of years dead a person is. Or -Infinity, if alive.
        """
        if self.date_of_death:
            return relativedelta(date.today(), self.date_of_death).years
        else:
            return float("-Inf")

    def full_name(self) -> str:
        return " ".join([self.first_name, self.last_name])
