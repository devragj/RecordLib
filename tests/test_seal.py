import pytest
from RecordLib.ruledefs.seal import *
from RecordLib.crecord import CRecord, Charge
import json
from RecordLib.serializers import to_serializable
from datetime import date

def test_seal(example_crecord):
    example_crecord.cases[0].fines_and_costs = 0
    example_crecord.cases[0].disposition_date = date(1990, 1, 1)
    example_crecord.cases[0].charges[0] = Charge(
        offense="Being silly",
        grade="M1",
        disposition="Guilty",
        statute="14 s 123",
        sentences=[],
    )
    mod_rec, analysis = seal_convictions(example_crecord, Decision("Seal convictions"))
    res = json.dumps(analysis, default=to_serializable, indent=4)
    assert len(analysis["Seal Convictions"].value["sealings"]) == 1


def test_no_danger_to_person_offense(example_crecord):
    example_crecord.cases[0].charges[0] = Charge(
        offense="Being silly",
        grade="M1",
        disposition="Guilty",
        statute="18 § 123",
        sentences=[],
    )
    decision = no_danger_to_person_offense(example_crecord, penalty_limit=7, conviction_limit=1, within_years=20)
    assert bool(decision.value) == True

    charge =  Charge(
        offense="Being silly",
        grade="M1",
        disposition="Guilty",
        statute="18 § 2301",
        sentences=[],
    )

    decision = no_danger_to_person_offense(charge, penalty_limit=2, conviction_limit=1, within_years=20)
    assert bool(decision.value) == False

def test_not_felony1(example_charge):
    example_charge.grade = "F1"
    example_charge.disposition = "Guilty"
    decision = not_felony1(example_charge)
    assert decision.value is False

    example_charge.disposition = "Not Guilty"
    decision = not_felony1(example_charge)
    assert decision.value is True
    assert decision.reasoning == "The charge was F1, but the disposition was Not Guilty"

    example_charge.grade = "M2"
    decision = not_felony1(example_charge)
    assert decision.value is True

    example_charge.grade = ""
    decision = not_felony1(example_charge)
    assert decision.value == False
    assert (
        decision.reasoning
        == "The charge's grade is unknown, so we don't know its *not* an F1."
    )

def test_ten_years_since_last_conviction(example_crecord):
    example_crecord.cases[0].disposition_date = date(1990, 1, 1)
    example_crecord.cases[0].charges[0].disposition = "Guilty"
    d = ten_years_since_last_conviction(example_crecord)
    assert d.value == True 

    example_crecord.cases[0].disposition_date = date.today()
    d = ten_years_since_last_conviction(example_crecord)
    assert d.value == False 


def test_offenses_punishable_by_two_or_more_years(example_crecord):
    example_crecord.cases[0].disposition_date = date.today()
    c1 =  Charge(
        offense="Being silly",
        grade="M1",
        disposition="Guilty",
        statute="18 § 2301",
        sentences=[],
    )
    c2 =  Charge(
        offense="Being sleepy",
        grade="F2",
        disposition="Guilty",
        statute="18 § 0987",
        sentences=[],
    )
    c3 =  Charge(
        offense="Being hungry",
        grade="M2",
        disposition="Guilty",
        statute="18 § 1111",
        sentences=[],
    )
    c4 =  Charge(
        offense="Being funny",
        grade="M2",
        disposition="Guilty",
        statute="18 § 1111",
        sentences=[],
    )
    example_crecord.cases[0].charges = [c1, c2, c3, c4]
    assert bool(offenses_punishable_by_two_or_more_years(example_crecord, conviction_limit=4, within_years=20)) == False
    example_crecord.cases[0].disposition_date = date(1950, 1, 1)
    assert bool(offenses_punishable_by_two_or_more_years(example_crecord, conviction_limit=4, within_years=20)) == True 

       

def test_no_offense_against_family(example_crecord):
    charge =  Charge(
        offense="Being silly",
        grade="M1",
        disposition="Guilty",
        statute="18 § 4301",
        sentences=[],
    )
    example_crecord.cases[0].charges[0] = charge
    d  = no_offense_against_family(example_crecord, penalty_limit=1, conviction_limit=1, within_years=50)
    assert bool(d) is False
    d  = no_offense_against_family(example_crecord, penalty_limit=1, conviction_limit=3, within_years=50)
    assert bool(d) is True
    example_crecord.cases[0].charges = [charge, charge, charge, charge]
    d  = no_offense_against_family(example_crecord, penalty_limit=1, conviction_limit=2, within_years=50)
    assert bool(d) is False


def test_no_paramilitary_training(example_crecord):
    example_crecord.cases[0].charges =  [Charge(
        offense="Being silly",
        grade="M1",
        disposition="Guilty",
        statute="18 § 5515",
        sentences=[],
    )]
    d = no_paramilitary_training(example_crecord, conviction_limit=1, within_years=15)
    assert bool(d) is False
    example_crecord.cases[0].disposition_date = date(1950, 1, 1)
    d = no_paramilitary_training(example_crecord, conviction_limit=1, within_years=15)
    assert bool(d) is True 

    example_crecord.cases[0].disposition_date = date.today()
    example_crecord.cases[0].charges.append(Charge(
        offense="eating ice cream",
        grade="M1",
        disposition="Guilty Plea",
        statute="18 § 1",
        sentences=[],
    ))
    d = no_paramilitary_training(example_crecord, conviction_limit=1, within_years=15)
    assert bool(d) is False 

@pytest.mark.skip("not tested yet")
def test_no_abuse_of_corpse(example_crecord):
    pass
 
@pytest.mark.skip("not tested yet")
def test_no_weapons_of_escape(example_crecord):
    pass

@pytest.mark.skip("not tested yet")
def test_no_failure_to_register(example_crecord):
    pass

@pytest.mark.skip("not tested yet")
def test_no_intercourse_w_animal(example_crecord):
    pass

@pytest.mark.skip("not tested yet")
def test_no_indecent_exposure(example_crecord):
    pass

 