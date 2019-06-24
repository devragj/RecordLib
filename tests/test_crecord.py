from RecordLib.crecord import CRecord
from RecordLib.common import Person
import pytest
from datetime import date

def test_init():
    dob = date(2010, 1,1)
    person = Person(**{
        "first_name": "Joe",
        "last_name": "Smith",
        "date_of_birth": dob
    })
    rec = CRecord(**{
        "person": person
    })
    assert rec.person.first_name == "Joe"
    rec = CRecord(
        person = Person(
            first_name="Joan",
            last_name="Smythe",
            date_of_birth=dob
        )
    )
    assert rec.person.last_name == "Smythe"


def test_years_since_last_arrested_or_prosecuted(example_crecord):
    example_crecord.years_since_last_arrested_or_prosecuted()


def test_years_since_final_release(example_crecord):
    example_crecord.years_since_final_release()

def test_init_empty_fails():
    """ Fail without a Person to relate the record to. """
    with pytest.raises(TypeError):
        rec = CRecord()


def test_invalid_schema():
    with pytest.raises(TypeError):
        CRecord(**{
            "persons": {
                "first_name": "Blank"
            }
        })
