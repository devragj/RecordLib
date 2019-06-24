from RecordLib import ruledefs
from datetime import date
import pytest

def test_rule_expunge_over_70(example_crecord):
    example_crecord.person.date_of_birth = date(1920, 1, 1)
    example_crecord.cases[0].arrest_date = date(1970, 1, 1)
    modified_record, analysis = ruledefs.expunge_over_70(example_crecord)
