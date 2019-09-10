from RecordLib.common import *
from dataclasses import asdict
from datetime import date, timedelta
import pytest

def test_person():
    per = Person("John", "Smeth", date(2010, 1, 1), date(2020, 1, 1))
    assert per.first_name == "John"
    assert per.last_name == "Smeth"
    assert per.date_of_birth.year == 2010
    assert per.date_of_death.year == 2020

def test_person_age():
    per = Person("John", "Smeth", date(2000, 1, 1))
    assert per.age() > 17


def test_person_years_dead(example_person):
    example_person.date_of_death = None
    assert example_person.years_dead() == float("-Inf")
    example_person.date_of_death = date.today()
    assert example_person.years_dead() == 0
    example_person.date_of_death = date(2000,1,1)
    assert example_person.years_dead() > 10


def test_person_todict():
    per = Person("John", "Smeth", date(2010, 1, 1))
    assert asdict(per) == {
        "first_name": "John",
        "last_name": "Smeth",
        "date_of_birth": date(2010, 1, 1),
        "date_of_death": None,
    }

def test_sentence():
    st = Sentence(
        sentence_date=date(2010, 1, 1),
        sentence_type="Probation",
        sentence_period="90 days",
        sentence_length=SentenceLength.from_tuples(
            min_time=("90", "Day"),
            max_time=("90", "Day")
        )
    )
    assert st.sentence_complete_date() == date(2010, 1, 1) + timedelta(days=90)

def test_calculate_days():
    assert SentenceLength.calculate_days("40", "Day(s)").days == 40
    assert SentenceLength.calculate_days("3 ", "Month(s)").days == 91
    assert SentenceLength.calculate_days(" 1", "Year(s)").days == 365
    assert SentenceLength.calculate_days(" Other", "Values") is None

def test_SentenceLength():
    lng = SentenceLength.from_tuples(
        min_time=("30", " Day(s)"),
        max_time=("1", "Year(s)")
    )
    assert lng.max_time.days==365
    assert lng.min_time.days==30

def test_charge():
    char = Charge(
        offense="Eating w/ mouth open",
        grade="M2",
        statute="24 &sect; 102",
        disposition="Guilty Plea",
        sentences=[])
    assert char.offense == "Eating w/ mouth open"
    assert char.grade == "M2"
    assert char.disposition == "Guilty Plea"


@pytest.mark.parametrize("disposition, is_a_conviction", (
    ("Guilty",True),
    ("Not Guilty",False),
    ("Nolle Prossed",False),
    ("Withdrawn",False),
    ("",False)
))
def test_charge_is_conviction(example_charge, disposition, is_a_conviction):
    example_charge.disposition = disposition
    assert example_charge.is_conviction() == is_a_conviction

def test_charge_get_section(example_charge):
    example_charge.statute = "18 § 1234"
    assert example_charge.get_statute_section() == 1234
    example_charge.statute = "18 § 4815.1"
    assert example_charge.get_statute_section() == 4815.1

def test_charge_get_chapter(example_charge):
    example_charge.statute = "18 § 1234"
    assert example_charge.get_statute_chapter() == 18

def test_charge_get_statute_subsections(example_charge):
    example_charge.statute = "75 § 3802 §§ A1*"
    assert example_charge.get_statute_subsections() == "A1*"

def test_charge_get_grade(example_charge):
    example_charge.statute = "10 § 162.12"

    # Grade doesn't change if its already set.
    example_charge.grade = "F1"
    assert example_charge.set_grade()
    assert example_charge.grade == "F1"

    # But if the grade is blank, then a new grade will be assigned.
    example_charge.grade = ""
    grade_decision = example_charge.set_grade()
    assert grade_decision.value == "M1"
    assert example_charge.grade == "M1"