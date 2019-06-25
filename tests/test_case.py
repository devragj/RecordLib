from RecordLib.case import Case
from RecordLib.common import Charge
import pytest
from datetime import date
from dataclasses import asdict


def test_case(example_sentence):
    char = Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea",
        sentences=[example_sentence])
    case = Case(
        status="Open",
        county="Erie",
        docket_number="12-CP-01",
        otn="112000111",
        dc="11222",
        charges=[char],
        fines_and_costs=200,
        judge="Smooth Operator",
        disposition_date=None,
        arrest_date=None
    )
    assert case.status == "Open"

def test_case_todict(example_case):
    assert example_case.to_dict()["county"] == example_case.county

@pytest.mark.parametrize(
        "arrest, disp, last",
    [
        (date(2019, 3, 1), date(2019, 4, 15), date(2019, 4, 15)),
        (date(2019, 4, 15), date(2019, 3, 1), date(2019, 4, 15)),
        (date(2019, 1, 1), None, date(2019, 1, 1)),
        (None, None, None)
    ])
def test_case_last_action(example_case, arrest, disp, last):
    example_case.arrest_date = arrest
    example_case.disposition_date = disp
    example_case.last_action() == last

def test_order_cases_by_last_action(example_case):
    # sorting when a case has no last_action fails.
    case2 = Case(
        status="Open",
        county="Erie",
        docket_number="12-CP-01",
        otn="112000111",
        dc="11222",
        charges=[example_case],
        fines_and_costs=200,
        judge="Smooth Operator",
        disposition_date=date(2019,1,1),
        arrest_date=None
    )
    with pytest.raises(TypeError):
        s = sorted([example_case, case2], key=Case.order_cases_by_last_action)

    example_case.arrest_date = date(2019,1,1)
    try:
        s = sorted([example_case, case2], key=Case.order_cases_by_last_action)
    except TypeError as e:
        pytest.fail(e)
