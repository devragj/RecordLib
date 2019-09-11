"""
Common, simple dataclasses live here.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
from datetime import date, timedelta
import re
import logging
from dateutil.relativedelta import relativedelta
import json
from RecordLib.decision import Decision
from RecordLib.guess_grade import guess_grade


@dataclass
class Person:
    """
    Track information about a person.
    """

    first_name: str
    last_name: str
    date_of_birth: date
    date_of_death: Optional[date] = None

    @staticmethod
    def from_dict(dct: dict) -> Person:
        """ Create a Person from a dict decribing one. """
        if dct is not None:
            return Person(
                first_name = dct.get("first_name"),
                last_name = dct.get("last_name"),
                date_of_birth = dct.get("date_of_birth"), 
                date_of_death = dct.get("date_of_death")
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


@dataclass
class SentenceLength:
    """
    Track info about the length of a sentence
    """

    min_time: timedelta
    max_time: timedelta

    @staticmethod
    def from_dict(dct: dict) -> SentenceLength:
        """
        Create a SentenceLength object from a dict.

        The dict will not have tuples as __init__ would expect, but rather four keys: 
        * min_unit
        * min_time
        * max_unit
        * max_time
        """
        slength = SentenceLength(
            (str(dct.get("min_time")), dct.get("min_unit")),
            (str(dct.get("max_time")), dct.get("max_unit")))
        return slength

    @staticmethod
    def calculate_days(length: str, unit: str) -> Optional[timedelta]:
        """
        Calculate the number of days represented by the pair `length` and `unit`.

        Sentences are often given in terms like "90 days" or "100 months".
        This method attempts to calculate the number of days that these phrases describe.

        Args:
            length (str): A string that can be converted to an integer
            unit (str): A unit of time, Days, Months, or Years
        """
        if length == "" or str == "":
            return timedelta(days=0)
        if re.match("day", unit.strip(), re.IGNORECASE):
            try:
                return timedelta(days=float(length.strip()))
            except ValueError:
                logging.error(f"Could not parse { length } to int")
                return None
        if re.match("month", unit.strip(), re.IGNORECASE):
            try:
                return timedelta(days=30.42 * float(length.strip()))
            except ValueError:
                logging.error(f"Could not parse { length } to int")
                return None
        if re.match("year", unit.strip(), re.IGNORECASE):
            try:
                return timedelta(days=365 * float(length.strip()))
            except ValueError:
                logging.error(f"Could not parse { length } to int")
                return None
        if unit.strip() != "":
            logging.warning(f"Could not understand unit of time: { unit }")
        return None

    @classmethod
    def from_tuples(cls, min_time: Tuple[str, str], max_time: Tuple[str, str]):
        """
        With two tuples in the form (time-as-string, unit),
        create an object that represents a length of a sentence.
        """
        min_time = SentenceLength.calculate_days(*min_time)
        max_time = SentenceLength.calculate_days(*max_time)
        return cls(min_time=min_time, max_time=max_time)


@dataclass
class Sentence:
    """
    Track information about a sentence. A Charge has zero or more Sentences.
    """

    sentence_date: date
    sentence_type: str
    sentence_period: str
    sentence_length: SentenceLength

    @staticmethod
    def from_dict(dct: dict) -> Sentence:
        dct["sentence_length"] = SentenceLength.from_dict(dct.get("sentence_length"))
        return Sentence(**dct)

    def sentence_complete_date(self):
        try:
            return self.sentence_date + self.sentence_length.max_time
        except:
            return None


@dataclass
class Charge:
    """
    Track information about a charge
    """

    offense: str
    grade: str
    statute: str
    disposition: str
    sentences: List[Sentence]

    @staticmethod
    def from_dict(dct: dict) -> Charge:
        try:
            dct["sentences"] = [Sentence.from_dict(s) for s in dct.get("sentences")] or []
            return Charge(**dct)
        except:
            return None

    def set_grade(self) -> Decision:
        """ Ensure the grade property of this Charge is set and return a decision explaining how it was set.

        Many charges are ungraded because of clerical deficiencies, especially in Philadelphia. 
        Knowing the grade of an offense is critical to many parts of an analysis. 

        If a charge already has a grade assigned, this function will simply return it. If the charge 
        does not yet have a grade assigned, then this function will assign one using a database to guess the 
        appropriate grade. 

        If the function cannot find the right grade, the empty string will be assigned. 

        The function will return a Decision explaining how it set the grade.
        """
        d = Decision(name=f"Grade for the offense, {self.statute}")
        if self.grade is not None and self.grade != "":
            d.value = self.grade
            d.reasoning = f"A grade of {self.grade} is already assigned."
        else:
            grades = guess_grade(self)
            self.grade = grades[0][0]
            d.value = self.grade
            d.reasoning = f"Assigned {self.grade}, with probablity {grades[0][1]}. Other possibilities are {grades[1:]}."
        return d

    def is_conviction(self) -> bool:
        """Is this charge a conviction?

        There are lots of different dispositions, and this helps identify if a disp. counts as a conviction or not.
        """
        if re.match("^Guilty", self.disposition.strip()):
            return True
        else:
            return False

    def get_statute_chapter(self) -> Optional[float]:
        patt = re.compile("^(?P<chapt>\d+)\s*§\s(?P<section>\d+).*")
        match = patt.match(self.statute)
        if match:
            return float(match.group("chapt"))
        else:
            return None

    def get_statute_section(self) -> Optional[float]:
        patt = re.compile("^(?P<chapt>\d+)\s*§\s(?P<section>\d+\.?\d*).*")
        match = patt.match(self.statute)
        if match:
            return float(match.group("section"))
        else:
            return None

    def get_statute_subsections(self) -> str:
        patt = re.compile("^(?P<chapt>\d+)\s*§\s(?P<section>\d+\.?\d*)\s*§§\s*(?P<subsections>[\(\)A-Za-z0-9\.\*]+)\s*.*")
        match = patt.match(self.statute)
        if match:
            return match.group("subsections")
        else:
            return ""
