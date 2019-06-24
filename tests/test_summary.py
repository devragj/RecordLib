from RecordLib.summary import Summary
from RecordLib.crecord import CRecord
from RecordLib.common import Person
import pytest
import os


def test_init():
    try:
        summary = Summary(
            pdf=open("tests/data/CourtSummaryReport.pdf", "rb"),
            tempdir="tests/data/tmp")
    except:
        pytest.fail("Creating Summary object failed.")

def test_parse_pdf_from_file():
    summary = Summary(
        pdf=open("tests/data/CourtSummaryReport.pdf", "rb"),
        tempdir="tests/data/tmp")
    assert len(summary.text) > 0

def test_parse_pdf_from_path():
    summary = Summary(
        pdf="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    assert len(summary._xml) > 0

def test_bulk_parse_pdf_from_path():
    paths = os.listdir("tests/data/summaries")
    if len(paths) == 0:
        pytest.fail("No summaries to parse in /tests/data/summaries.")
    for path in paths:
        try:
            summary = Summary(path, tempdir = "tests/data/tmp")
        except:
            pytest.fail(f"Failed to parse: {path}")
        assert len(summary._xml) > 0

def test_add_summary_to_crecord():
    summary = Summary(
        pdf="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    rec = CRecord(Person("John", "Smith"))
    rec.add_summary(summary)
    rec.person.first_name == summary._xml.xpath("caption/defendant_name")[0].text

def test_get_name():
    summary = Summary(
        pdf="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    assert len(summary.get_defendant_name().first_name) > 0
    assert len(summary.get_defendant_name().last_name) > 0

def test_get_cases():
    summary = Summary(
        pdf="tests/data/CourtSummaryReport.pdf",
        tempdir="tests/data/tmp")
    assert len(summary.get_cases()) > 0
    assert len(summary.get_cases()) > 0
    assert summary.get_cases()[0] is not None
