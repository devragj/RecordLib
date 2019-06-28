from RecordLib import ruledefs
from RecordLib.common import Sentence, SentenceLength
from datetime import date
import pytest
import types

def test_rule_expunge_over_70(example_crecord):
    example_crecord.person.date_of_birth = date(1920, 1, 1)
    example_crecord.cases[0].arrest_date = date(1970, 1, 1)
    example_crecord.cases[0].charges[0].sentences = [Sentence(
        sentence_date = date.today(),
        sentence_type = "Confinement",
        sentence_period = "90 days",
        sentence_length = SentenceLength(("90","day"), ("90","day"))
    )]
    modified_record, analysis = ruledefs.expunge_over_70(example_crecord)
    assert analysis["age_over_70_expungements"]["conclusion"] == "No expungements possible"
    assert analysis["age_over_70_expungements"]["conditions"]["years_since_final_release"] == False
    assert len(modified_record.cases) == len(example_crecord.cases)

    example_crecord.cases[0].charges[0].sentences[0] = Sentence(
        sentence_date = date(1980, 1, 1),
        sentence_type = "Confinement",
        sentence_period = "90 days",
        sentence_length = SentenceLength(("90","day"), ("90","day"))
    )
    modified_record, analysis = ruledefs.expunge_over_70(example_crecord)
    assert analysis["age_over_70_expungements"]["conclusion"] == "Expunge cases"
    analysis["age_over_70_expungements"]["conditions"]["years_since_final_release"] == True
    # The modified record has removed the cases this rule wants to expunge.
    assert len(modified_record.cases) < len(example_crecord.cases)
