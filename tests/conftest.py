import pytest
from RecordLib.case import Case
from RecordLib.common import Charge, Person, Sentence, SentenceLength
from RecordLib.crecord import CRecord
from RecordLib.summary import Summary
from datetime import date

@pytest.fixture
def example_summary():
    return Summary("tests/data/CourtSummaryReport.pdf", tempdir="tests/data/tmp")

@pytest.fixture
def example_person():
    return Person(
        first_name="Jane",
        last_name="Smorp",
        date_of_birth=date(2010, 1, 1)
    )

@pytest.fixture
def example_sentencelength():
    return SentenceLength(
        min_time=("10","Year"),
        max_time=("25", "Year")
    )

@pytest.fixture
def example_sentence(example_sentencelength):
    return Sentence(
        sentence_date=date(2000,1,1),
        sentence_type="Confinement",
        sentence_period="180 days",
        sentence_length=example_sentencelength
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
