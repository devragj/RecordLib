from RecordLib.crecord import CRecord
from RecordLib.common import Person
import pytest


def test_init():
    person = Person(**{
        "first_name": "Joe",
        "last_name": "Smith"
    })
    rec = CRecord(**{
        "person": person
    })
    assert rec.person.first_name == "Joe"
    rec = CRecord(
        person = Person(
            first_name="Joan",
            last_name="Smythe"
        )
    )
    assert rec.person.last_name == "Smythe"


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
