from RecordLib.docket import Docket
import pytest

def test_init():
    try:
        dk = Docket()
    except:
        pytest.fail("Cannot create Docket object")
