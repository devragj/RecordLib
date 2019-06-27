"""
Common, simple dataclasses live here.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Tuple
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

class SentenceLength:
    """
    Track info about the length of a sentence
    """
    min_length: int
    max_length: int

    def __init__(self, min_length: Tuple[str], max_length: Tuple[str]):
        """
        With two tuples in the form (time-as-string, unit),
        create an object that represents a length of a sentence.
        """
        

@dataclass
class Sentence:
    """
    Track information about a sentence. A Charge has zero or more Sentences.
    """
    sentence_date: date
    sentence_type: str
    sentence_period: str
    sentence_length: SentenceLength

    def sentence_complete(self):
        try:
            min = self.sentence_length.get("min_length")
            max = self.sentence
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
