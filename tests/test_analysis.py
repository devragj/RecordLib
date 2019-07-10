from RecordLib.analysis import Analysis
from RecordLib.ruledefs import (
    expunge_over_70, expunge_summary_convictions
)
import pytest




def test_init(example_crecord):
    try:
        ans = Analysis(example_crecord)
    except:
        pytest.fail("Could not create analysis object")

def test_rule(example_crecord):
    ans = Analysis(example_crecord)
    try:
        ans.rule(expunge_summary_convictions)
    except:
        pytest.fail("Could not apply rule to record.")

def test_rule_chaining(example_crecord):
    ans = Analysis(example_crecord)
    try:
        (ans
         .rule(expunge_over_70)
         .rule(expunge_summary_convictions)
        )
    except:
        pytest.fail("Could not chain analysis rule operations.")
