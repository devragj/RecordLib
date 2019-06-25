"""
Common, simple dataclasses live here.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List
import functools
from datetime import date
import pytest

@dataclass
class Person:
    """
    Track information about a person.
    """

    first_name: str
    last_name: str
    date_of_birth: date

    def age(self) -> int:
        """ Age in years """
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day))

@dataclass
class Sentence:
    """
    Track information about a sentence. A Charge has zero or more Sentences.
    """
    sentence_date: date
    sentence_type: str
    sentence_period: str
    sentence_length: str

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
