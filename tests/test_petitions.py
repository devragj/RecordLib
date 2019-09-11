

from RecordLib.petitions import Petition, Expungement, Sealing


def test_petition(example_person, example_case):
    p = Petition(person=example_person, cases=[example_case])
    assert p.cases[0] == example_case

def test_expungement_petition(example_person, example_case):
    p = Expungement(person=example_person, cases=[example_case])
    assert p.cases[0] == example_case
    

def test_sealing_petition(example_person, example_case):
    p = Sealing(person=example_person, cases=[example_case])
    assert p.cases[0] == example_case