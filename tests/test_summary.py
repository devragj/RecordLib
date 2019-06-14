from RecordLib.summary import Summary
import pytest



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
