from RecordLib.summary import Summary
import pytest



def test_init():
    try:
        summary = Summary(pdf=open("tests/data/CourtSummaryReport.pdf", "rb"))
    except:
        pytest.fail("Creating Summary object failed.")

def test_parse_pdf():
    summary = Summary(pdf=open("tests/data/CourtSummaryReport.pdf", "rb"))
    assert len(summary.text) > 0
