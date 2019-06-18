from RecordLib.crecord import CRecord
import pytest


def test_init():
    rec = CRecord(data = {
        "person": {
            "first_name": "Joe",
            "last_name": "Smith"
        }
    })
    #pytest.set_trace()
    assert rec.person.first_name == "Joe"


def test_init_empty():
    try:
        rec = CRecord()
    except:
        pytest.fail("Should not have failed.")


def test_invalid_schema():
    with pytest.raises(AssertionError):
        CRecord({
            "persons": {
                "first_name": "Blank"
            }
        })
