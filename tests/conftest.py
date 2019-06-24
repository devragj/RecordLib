import pytest
from RecordLib.common import Case, Charge, Person
from RecordLib.crecord import CRecord
from datetime import date

@pytest.fixture
def example_person():
    return Person(
        first_name="Jane",
        last_name="Smorp",
        date_of_birth=date(2010, 1, 1)
    )

@pytest.fixture
def example_charge():
    return Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea")

@pytest.fixture
def example_case(example_charge):
    return Case(
        status="Open",
        county="Erie",
        docket_numbers=["12-CP-01", "12-MC-01"],
        otn="112000111",
        dc="11222",
        charges=[example_charge],
        fines_and_costs=200,
        arrest_date=None,
        disposition_date=None,
        judge="Judge Jimmy Hendrix"
    )


@pytest.fixture
def example_crecord(example_person, example_case):
    return CRecord(
        person=example_person,
        cases = [example_case])
