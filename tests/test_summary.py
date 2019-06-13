from RecordLib.summary import Summary
import pytest



def test_init():
    try:
        summary = Summary()
    except:
        pytest.fail("Creating Summary object failed.")
