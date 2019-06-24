import pytest
from RecordLib.common import Case, Charge


@pytest.fixture
def example_charge():
    return Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea")

@pytest.fixture
def example_case(example_charge):
    return Case(
        status="Open",
        county="Erie",
        docket_numbers=["12-CP-01", "12-MC-01"],
        otn="112000111",
        dc="11222",
        charges=[example_charge],
        fines_and_costs=200
    )
