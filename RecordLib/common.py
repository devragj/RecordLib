"""
Common, simple dataclasses live here.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, is_dataclass
from typing import List, Tuple
import functools
from datetime import date, datetime
import pytest
import re
import logging
from datetime import timedelta
from typing import Optional
from dateutil.relativedelta import relativedelta
import json

@dataclass
class Person:
    """
    Track information about a person.
    """

    first_name: str
    last_name: str
    date_of_birth: date
    date_of_death: Optional[date] = None

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

class SentenceLength:
    """
    Track info about the length of a sentence
    """

    min_time: timedelta
    max_time: timedelta

    @staticmethod
    def calculate_days(length: str, unit: str) -> float:
        """
        Calculate the number of days represented by the pair `length` and `unit`.

        Sentences are ovent given in terms like "90 days" or "100 months". This method attempts to calculate the number of days that these phrases describe.

        Args:
            length (str): A string that can be converted to an integer
            unit (str): A unit of time, Days, Months, or Years
        """
        if length == "" or str == "":
            return(timedelta(days=0))
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

    def __init__(self, min_time: Tuple[str], max_time: Tuple[str]):
        """
        With two tuples in the form (time-as-string, unit),
        create an object that represents a length of a sentence.
        """
        self.min_time = SentenceLength.calculate_days(*min_time)
        self.max_time = SentenceLength.calculate_days(*max_time)


@dataclass
class Sentence:
    """
    Track information about a sentence. A Charge has zero or more Sentences.
    """

    sentence_date: date
    sentence_type: str
    sentence_period: str
    sentence_length: SentenceLength

    def sentence_complete_date(self):
        try:
            return self.sentence_length.max_time + self.sentence_date
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

@functools.singledispatch
def to_serializable(val):
    """
    single_dispatch is for letting me define how different classes should serialize.

    There's a single default serializer (this method), and then additional methods that replace this method depending on the type sent to the method.
    """
    return str(val)

@to_serializable.register(Charge)
def ts_charge(charge):
    return asdict(charge)

@to_serializable.register(date)
@to_serializable.register(datetime)
def ts_date(a_date):
    return a_date.isoformat()
