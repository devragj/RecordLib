import pytest
from RecordLib.case import Case
from RecordLib.person import Person
from RecordLib.common import Charge, Sentence, SentenceLength
from RecordLib.crecord import CRecord
from RecordLib.attorney import Attorney
from RecordLib.summary.pdf import parse_pdf as parse_summary_pdf
from RecordLib.docket import Docket
from datetime import date
import redis
from RecordLib.redis_helper import RedisHelper
import os
#from django.test import Client 
from rest_framework.test import APIClient

@pytest.fixture
def example_attorney():
        return Attorney(
                organization = "Community Legal",
                full_name = "John Smith",
                organization_address = r"1234 Main St.\nBig City, NY 10002",
                organization_phone = "555-555-5555",
                bar_id = "123456",
              )

@pytest.fixture
def example_summary():
    return parse_summary_pdf(
        pdf="tests/data/CourtSummaryReport.pdf", tempdir="tests/data/tmp")

@pytest.fixture
def example_docket():
    docket_path = os.listdir("tests/data/dockets")[0]
    d, errs = Docket.from_pdf(os.path.join("tests","data","dockets",docket_path), tempdir="tests/data/tmp")
    return d

@pytest.fixture
def example_person():
    return Person(
        first_name="Jane",
        last_name="Smorp",
        aliases=["JSmo", "SmorpyJJ"],
        address="1234 Main St",
        date_of_birth=date(2010, 1, 1),
        ssn="999-99-9999",
    )

@pytest.fixture
def example_sentencelength():
    return SentenceLength.from_tuples(
        min_time=("10", "Year"),
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
        disposition_date=date(2010,1,1),
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
        total_fines=200,
        fines_paid=100,
        arrest_date=None,
        complaint_date=None,
        disposition_date=None,
        judge="Judge Jimmy Hendrix",
        judge_address="1234 Judge St.,",
        affiant="Officer Bland",
        arresting_agency_address="1234 Grey St.",
        arresting_agency="Monochrome County PD."
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


@pytest.fixture
def dclient():
    """ Django test client """
    return APIClient()