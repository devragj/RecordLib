import pytest
from RecordLib.common import Case, Charge, Person, Sentence
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
def example_sentence():
    return Sentence(
        sentence_date=date(2000,1,1),
        sentence_type="Confinement",
        sentence_period="180 days",
        sentence_length="Min 180 days, max 365 days"
    )

@pytest.fixture
def example_charge(example_sentence):
    return Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea",
        sentences=[example_sentence])

@pytest.fixture
def example_case(example_charge):
    return Case(
        status="Open",
        county="Erie",
        docket_number="12-CP-01",
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
