import pytest
from RecordLib.case import Case
from RecordLib.common import Charge, Person, Sentence, SentenceLength
from RecordLib.crecord import CRecord
from RecordLib.summary.pdf import parse_pdf as parse_summary_pdf
from datetime import date
import redis
from RecordLib.redis_helper import RedisHelper

@pytest.fixture
def example_summary():
    return parse_summary_pdf(
        pdf="tests/data/CourtSummaryReport.pdf", tempdir="tests/data/tmp")

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
        docket_number="12-MC-01",
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

@pytest.fixture
def redis_helper():
    """ A redis client.

    N.B. I don't know a way for this fixture to yield r and the rollback whatever a test does with the database. So tests using this fixture need to roll themselves back.
    """
    redis_helper = RedisHelper(host='localhost', port=6379, db=0,decode_responses=True, env="test")
    yield redis_helper
    for key in redis_helper.r.scan_iter("test:*"):
        redis_helper.r.delete(key)
