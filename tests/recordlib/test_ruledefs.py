

from RecordLib import ruledefs
from RecordLib.ruledefs.seal import (
    not_felony1, fines_and_costs_paid, is_misdemeanor_or_ungraded)
from RecordLib.common import Sentence, SentenceLength
from RecordLib.case import Case
from RecordLib.serializers import to_serializable
from RecordLib.petitions import Expungement
from datetime import date
import pytest
import types
import copy

def test_rule_expunge_over_70(example_crecord):
    example_crecord.person.date_of_birth = date(1920, 1, 1)
    example_crecord.cases[0].arrest_date = date(1970, 1, 1)
    example_crecord.cases[0].charges[0].sentences = [Sentence(
        sentence_date=date.today(),
        sentence_type="Confinement",
        sentence_period="90 days",
        sentence_length=SentenceLength.from_tuples(("90","day"), ("90","day"))
    )]
    remaining_recordord, analysis = ruledefs.expunge_over_70(example_crecord)
    assert analysis.value == []
    assert [bool(d) for d in analysis.reasoning] == [True, True, False]
    assert len(remaining_recordord.cases) == len(example_crecord.cases)

    example_crecord.cases[0].charges[0].sentences[0] = Sentence(
        sentence_date=date(1980, 1, 1),
        sentence_type="Confinement",
        sentence_period="90 days",
        sentence_length=SentenceLength.from_tuples(("90", "day"), ("90", "day"))
    )
    remaining_recordord, analysis = ruledefs.expunge_over_70(example_crecord)
    assert isinstance(analysis.value[0], Expungement)
    # The modified record has removed the cases this rule wants to expunge.
    assert len(remaining_recordord.cases) < len(example_crecord.cases)


def test_expunge_deceased(example_crecord):
    example_crecord.person.date_of_death = None
    mod_rec, analysis = ruledefs.expunge_deceased(example_crecord)
    assert analysis.value == []

    example_crecord.person.date_of_death = date(2000, 1, 1)
    mod_rec, analysis = ruledefs.expunge_deceased(example_crecord)
    assert len(analysis.value) == len(example_crecord.cases)


def test_expunge_summary_convictions(example_crecord, example_charge):
    # Old summary convictions are expungeable
    example_crecord.cases[0].charges[0].grade = "S"
    example_crecord.cases[0].arrest_date = date(2000, 1, 1)
    example_crecord.cases[0].disposition_date = date(2001, 1, 1)
    mod_rec, analysis = ruledefs.expunge_summary_convictions(example_crecord)
    assert len(analysis.value) == len(example_crecord.cases)

    # no expunged summary convictions if there was a recent arrest.
    example_crecord.cases[0].arrest_date = date(2019, 1, 1)
    mod_rec, analysis = ruledefs.expunge_summary_convictions(example_crecord)
    assert len(analysis.value) == 0

    # Only summary convictions, not other grades, can be expunged.
    new_charge = copy.deepcopy(example_charge)
    new_charge.grade = "M2"
    example_crecord.cases[0].arrest_date = date(2000, 1, 1)
    example_crecord.cases[0].charges.append(new_charge)
    assert len(example_crecord.cases[0].charges) == 2

    mod_rec, analysis = ruledefs.expunge_summary_convictions(
        example_crecord)
    assert len(analysis.value) == 1
    assert len(mod_rec.cases) == 1

@pytest.mark.parametrize("disp", [(""), ("Nolle Prossed"), ("Withdrawn"), ("Not Guilty")])
def test_expunge_nonconvictions(example_crecord, example_charge, disp):
    example_crecord.cases[0].charges[0].disposition = disp
    mod_rec, analysis = ruledefs.expunge_nonconvictions(example_crecord)
    assert len(analysis.value) == len(example_crecord.cases)
    assert len(mod_rec.cases) == 0


