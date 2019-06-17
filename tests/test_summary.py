from RecordLib.summary import Summary
import pytest
import os


def test_init():
    try:
        summary = Summary(pdf=open("tests/data/CourtSummaryReport.pdf", "rb"))
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
    assert len(summary.text) > 0

def test_bulk_parse_pdf_from_path():
    paths = os.listdir("tests/data/summaries")
    if len(paths) == 0:
        pytest.fail("No summaries to parse in /tests/data/summaries.")
    for path in paths:
        try:
            Summary(path, tempdir = "tests/data/tmp")
        except:
            pytest.fail(f"Failed to parse: {path}")
