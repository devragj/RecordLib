from RecordLib.common import *
from dataclasses import asdict
from datetime import date
import pytest

def test_person():
    per = Person("John", "Smeth", date(2010, 1, 1))
    assert per.first_name == "John"
    assert per.last_name == "Smeth"

def test_person_age():
    per = Person("John", "Smeth", date(2000, 1, 1))
    assert per.age() > 17

def test_person_todict():
    per = Person("John", "Smeth", date(2010, 1, 1))
    assert asdict(per) == {
        "first_name": "John",
        "last_name": "Smeth",
        "date_of_birth": date(2010, 1, 1)
    }

def test_charge():
    char = Charge(
        offense="Eating w/ mouth open",
        grade="M2",
        statute="24 &sect; 102",
        disposition="Guilty Plea",)
    assert char.offense == "Eating w/ mouth open"
    assert char.grade == "M2"
    assert char.disposition == "Guilty Plea"

def test_case():
    char = Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea")
    case = Case(
        status="Open",
        county="Erie",
        docket_numbers=["12-CP-01", "12-MC-01"],
        otn="112000111",
        dc="11222",
        charges=[char],
        fines_and_costs=200,
        judge="Smooth Operator"
    )
    assert case.status == "Open"

def test_case_todict(example_case):
    assert example_case.to_dict()["county"] == example_case.county

@pytest.mark.parametrize(
        "arrest, disp, last",
    [
        (date(2019, 3, 1), date(2019, 4, 15), date(2019, 4, 15)),
        (date(2019, 4, 15), date(2019, 3, 1), date(2019, 4, 15)),
        (date(2019, 1, 1), None, date(2019, 1, 1)),
        (None, None, None)
    ])
def test_case_last_action(example_case, arrest, disp, last):
    example_case.arrest_date = arrest
    example_case.disposition_date = disp
    example_case.last_action() == last
