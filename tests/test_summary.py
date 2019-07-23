from RecordLib.summary import Summary
from RecordLib.summary.pdf import parse_pdf
from RecordLib.crecord import CRecord
from RecordLib.common import Person
from RecordLib.case import Case
import pytest
import os
from datetime import date, timedelta
import logging

def test_init():
    try:
        summary = Summary(
            parser=parse_pdf,
            raw_source=open("tests/data/CourtSummaryReport.pdf", "rb"),
            tempdir="tests/data/tmp")
    except:
        pytest.fail("Creating Summary object failed.")

def test_parse_pdf_from_file():
    summary = Summary(
        parser=parse_pdf,
        raw_source=open("tests/data/CourtSummaryReport.pdf", "rb"),
        tempdir="tests/data/tmp")
    assert len(summary.get_cases()) > 0

def test_parse_pdf_from_path():
    summary = Summary(
        parser=parse_pdf,
        raw_source="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    assert len(summary.get_cases()) > 0

def test_bulk_parse_pdf_from_path(caplog):
    caplog.set_level(logging.INFO)
    paths = os.listdir("tests/data/summaries")
    if len(paths) == 0:
        pytest.fail("No summaries to parse in /tests/data/summaries.")
    fails = []
    logging.info("Successful parses:")
    for path in paths:
        try:
            summary = Summary(parse_pdf, os.path.join(f"tests/data/summaries", path), tempdir="tests/data/tmp")
            logging.info(path)
        except:
            print(path)
            fails.append(os.path.split(path)[1])
    if len(fails) > 0:
        logging.error(f"{ len(fails) } / {len(paths)} summaries failed to parse:")
        for fail in fails:
            logging.error(f"  - {fail}")
        pytest.fail("Summaries failed to parse.")


def test_add_summary_to_crecord():
    summary = Summary(
        parse_pdf,
        raw_source="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    rec = CRecord(Person("John", "Smith", date(1998, 1, 1)))
    rec.add_summary(summary, override_person=True)
    assert len(rec.person.first_name) > 0
    assert rec.person.first_name != "John"

def test_get_defendant():
    summary = Summary(
        parse_pdf,
        raw_source="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    assert len(summary.get_defendant().first_name) > 0
    assert len(summary.get_defendant().last_name) > 0
    assert summary.get_defendant().date_of_birth > date(1900, 1, 1)

def test_get_cases():
    summary = Summary(
        parse_pdf,
        raw_source="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    assert len(summary.get_cases()) > 0
    assert len(summary.get_cases()) > 0
    assert isinstance(summary.get_cases()[0], Case)

def test_get_sentences():
    summary = Summary(
        parse_pdf,
        raw_source="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    cases = summary.get_cases()
    for case in cases:
        for charge in case.charges:
            for sentence in charge.sentences:
                try:
                    assert (isinstance(sentence.sentence_length.max_time, timedelta) or sentence.sentence_length.max_time is None)
                except:
                    pytest.fail("Could not get sentence from charge.")
