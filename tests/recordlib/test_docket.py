from RecordLib.docket import Docket
from RecordLib.person import Person
from RecordLib.case import Case
import pytest
import os
import logging

def test_pdf_factory_one():
    try:
        filename = os.listdir("tests/data/dockets")[0]
        dk, _ = Docket.from_pdf(os.path.join("tests/data/dockets", filename), tempdir="tests/data/tmp")
    except:
        pytest.fail("Cannot create Docket object")
    assert isinstance(dk._case, Case)
    assert isinstance(dk._defendant, Person)
    assert dk._case.affiant is not None
    assert dk._defendant.aliases is not None
    assert dk._case.arresting_agency is not None



def test_pdf_factory_bulk(caplog):
    """
    Test parsing a whole directory of dockets.

    N.B. This doesn't currently report a failure if a _section_ of a docket failed to parse. 

    Run w/ `pytest tests/test_docket.py -k bulk -v -o log_cli=true` to show logging, even when test
    doesn't fail. Useful because sections can fail w/out causing the test to fail.
    """
    caplog.set_level(logging.INFO)
    files = os.listdir("tests/data/dockets")
    total_dockets = len(files)
    successes = 0
    error_list = []
    for f in files:
        try:
            logging.info(f"Parsing {f}")
            _, errs = Docket.from_pdf(os.path.join("tests/data/dockets", f), tempdir="tests/data/tmp")
            if len(errs) > 0:
                error_list = error_list + [(f, errs)]
            successes += 1
            logging.info(f"    {f} parsed.")
        except Exception as e:
            logging.error(f"    {f} failed to parse.")
    
    if len(error_list) > 0:
        logging.error(f"{len(error_list)} cases had non-fatal parsing errors.")
        pytest.fail(f"{len(error_list)} cases had non-fatal parsing errors.")
    if successes < total_dockets:
        logging.error(f"Only {successes}/{total_dockets} parsed.")
        pytest.fail(f"Only {successes}/{total_dockets} parsed.")