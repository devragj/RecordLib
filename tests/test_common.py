from RecordLib.common import *



def test_person():
    per = Person("John", "Smeth")
    assert per.first_name == "John"
    assert per.last_name == "Smeth"

def test_charge():
    char = Charge(
        "Eating w/ mouth open",
        "M2", "Guilty Plea")
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

def test_caselist():
    char1 = Charge(
        "Eating w/ mouth open",
        "M2",
        "14 section 23",
        "Guilty Plea")
    char2 = Charge(
        "Sleeping in",
        "F1",
        "14 section 23",
        "Nolle Prossed"
    )
    case1 = Case(
        status="Open",
        county="Erie",
        docket_numbers=["12-MC-01"],
        otn="112000111",
        dc="11222",
        charges=[char1],
        fines_and_costs=200
    )
    case2 = Case(
        status="Open",
        county="Erie",
        docket_numbers=["13-CP-01"],
        otn="112000111",
        dc="11222",
        charges=[char2],
        fines_and_costs=300
    )
    cases = CaseList()
    cases.add(case1)
    cases.add(case2)
    len(cases) == 1
    len(cases[0].docket_numbers) == 2
    len(cases[0].charges) == 2
    cases[0].fines_and_costs == 500
