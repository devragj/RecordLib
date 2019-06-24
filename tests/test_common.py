from RecordLib.common import *



def test_person():
    per = Person("John", "Smeth")
    assert per.first_name == "John"
    assert per.last_name == "Smeth"

def test_charge():
    char = Charge(
        offense="Eating w/ mouth open",
        grade="M2",
        statute="24 &sect; 102",
        disposition="Guilty Plea",)
    assert char.offense == "Eating w/ mouth open"
    assert char.grade == "M2"
    assert char.disposition == "Guilty Plea"

def test_case():
    char = Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea")
    case = Case(
        status="Open",
        county="Erie",
        docket_numbers=["12-CP-01", "12-MC-01"],
        otn="112000111",
        dc="11222",
        charges=[char],
        fines_and_costs=200
    )
    assert case.status == "Open"
