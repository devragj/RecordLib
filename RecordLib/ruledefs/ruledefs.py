"""
Collect rule-functions that take a record and return an analysis of
how the rule applies to the record.

18 Pa.C.S. 9122 deals with Expungements
https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm?txtType=HTM&ttl=18&div=0&chpt=91



Ruledefs return Decisions of the type

Decision
    name: str,
    value: [Petition],
    reasoning: [Decision]

Simple Decisions have the type

Decision:
    name: str
    value: bool
    reasoning: [Decision] | str


"""
from RecordLib.crecord import CRecord
from RecordLib.person import Person
from RecordLib.decision import Decision
from RecordLib.petitions import Expungement, Sealing
import copy
from typing import Tuple
from dateutil.relativedelta import relativedelta
from datetime import date
import re

def is_over_age(person: Person, age_limit: int) -> Decision:
    return Decision(
        name=f"Is {person.first_name} over {age_limit}?",
        value=person.age() > 70,
        reasoning=f"{person.first_name} is {person.age()}"
    )

def years_since_last_contact(crec: CRecord, year_min: int) -> Decision:
    return Decision(
        name=f"Has {crec.person.first_name} been free of arrest or prosecution for {year_min} years?",
        value=crec.years_since_last_arrested_or_prosecuted() >= 10,
        reasoning=f"It has been {crec.years_since_last_arrested_or_prosecuted()} years."
    )

def years_since_final_release(crec: CRecord, year_min: int) -> Decision:
    return Decision(
        name=f"Has it been at least {year_min} years since {crec.person.first_name}'s final release from custody?",
        value=crec.years_since_final_release() > year_min,
        reasoning=f"It has been {crec.years_since_final_release()}."
    )


def expunge_over_70(crecord: CRecord) -> Tuple[CRecord, Decision]:
    """
    Analyze a crecord for expungements if the defendant is over 70.

    18 Pa.C.S. 9122(b)(1) provides for expungements of an individual who
    is 70 or older, and has been free of arrest or prosecution for 10
    years following the final release from confinement or supervision.
    """
    conclusion = Decision(
        name = "A record can be expunged for a person over 70.",
        reasoning = [
            is_over_age(crecord.person, 70),
            years_since_last_contact(crecord, 10),
            years_since_final_release(crecord, 10)
        ]
    ) 

    if all(conclusion.reasoning):
        exps = [Expungement(client=crecord.person, cases=[c], 
                            summary_expungement_language="and the Petitioner is over 70 years old has been free of arrest or prosecution for ten years following from completion the sentence") for c in crecord.cases]
        for e in exps:
            e.expungement_type = Expungement.ExpungementTypes.FULL_EXPUNGEMENT
        conclusion.value = exps
        remaining_recordord = CRecord(person=copy.deepcopy(crecord.person), cases=[])
    else:
        conclusion.value = []
        remaining_recordord = crecord
    
    return remaining_recordord, conclusion


def expunge_deceased(crecord: CRecord) -> Tuple[CRecord, Decision]:
    """
    Analyze a crecord for expungments if the individual has been dead for three years.

    18 Pa.C.S. 9122(b)(2) provides for expungement of records for an individual who has been dead for three years.
    """
    conclusion = Decision(
        name="A deceased person's record can be expunged after three years.",
        reasoning = [Decision(
            name=f"Has {crecord.person.first_name} been deceased for 3 years?",
            value=crecord.person.years_dead() > 3,
            reasoning=f"{crecord.person.first_name} is not dead, as far as I know." if crecord.person.years_dead() < 0 else f"It has been {crecord.person.years_dead()} since {crecord.person.first_name}'s death."
        )]
    )

    if all(conclusion.reasoning):
        exps = [Expungement(crecord.person, c) for c in crecord.cases]
        for e in exps:
            e.expungement_type = Expungement.ExpungementTypes.FULL_EXPUNGEMENT
        conclusion.value = exps
        remaining_recordord = CRecord(person=copy.deepcopy(crecord.person), cases=[])
    else:
        conclusion.value = []
        remaining_recordord = crecord

    return remaining_recordord, conclusion


def expunge_summary_convictions(
    crecord: CRecord
) -> Tuple[CRecord, Decision]:
    """
    Analyze crecord for expungements of summary convictions.

    18 Pa.C.S. 9122(b)(3)(i) and (ii) provide for expungement of summary convictions if the individual has been free of arrest or prosecution for five years following the conviction for the offense.

    Not available if person got ARD for certain offenses listed in (b.1)

    Returns:
        The function creates a Decision. The Value of the decision is a list of the Petions that can be
        generated according to this rule. The Reasoning of the decision is a list of decisions. The first
        decision is the global requirement for any expungement under this rule. The following decisions
        are a decision about the expungeability of each case. Each case-decision, contains its own explanation
        of what charges were or were not expungeable.  

    TODO excluding ARD offenses from expungements here.

    TODO grades are often missing. We should tell users we're uncertain.
    """
    # Initialize the decision explaining this rule's outcome. It starts with reasoning that includes the 
    # decisions that are conditions of any case being expungeable.
    conclusion = Decision(
        name="Expungements for summary convictions.",
        value=[],
        reasoning=[Decision(
            name=f"Has {crecord.person.first_name} been arrest free and prosecution free for five years?",
            value=crecord.years_since_last_arrested_or_prosecuted() > 5,
            reasoning=f"It has been {crecord.years_since_last_arrested_or_prosecuted()} since the last arrest or prosecection."
        )]
    )

    # initialize a blank crecord to hold the cases and charges that can't be expunged under this rule.
    remaining_recordord = CRecord(person=crecord.person)
    if all(conclusion.reasoning):
        for case in crecord.cases:
            # Find expungeable charges in a case. Save a Decision explaining what's expungeable to 
            # the reasoning of the Decision about the whole record.
            case_d = Decision(name=f"Is {case.docket_number} expungeable?", reasoning=[])
            expungeable_case = case.partialcopy() # The charges in this case that are expungeable.
            not_expungeable_case = case.partialcopy() # Charges in this case that are not expungeable.
            for charge in case.charges:
                charge_d = Decision(
                    name=f"Is this charge for {charge.offense} a summary conviction?",
                    reasoning=[
                        Decision(
                            name=f"Is this charge for {charge.offense} a summary?", 
                            value=charge.grade.strip() == "S",
                            reasoning=f"The charge's grade is {charge.grade.strip()}"),
                        Decision(
                            name=f"Is this charge for {charge.offense} a conviction?",
                            value=charge.is_conviction(),
                            reasoning=f"The charge's disposition {charge.disposition} indicates a conviction" if charge.is_conviction() else f"The charge's disposition {charge.disposition} indicates its not a conviction.")
                    ])
                if all(charge_d.reasoning):
                    expungeable_case.charges.append(charge)
                    charge_d.value = True
                else:
                    charge_d.value = False
                    not_expungeable_case.charges.append(charge)
                case_d.reasoning.append(charge_d)
    
            # If there are any expungeable charges, add an Expungepent to the Value of the decision about
            # this whole record.
            if len(expungeable_case.charges) > 0:
                case_d.value = True
                exp = Expungement(client=crecord.person, cases=[expungeable_case], 
                                  summary_expungement_language=".  The petitioner has been arrest free for more than five years since this summary conviction")
                if len(expungeable_case.charges) == len(case.charges):
                    exp.expungement_type = Expungement.ExpungementTypes.FULL_EXPUNGEMENT
                else:
                    exp.expungement_type = Expungement.ExpungementTypes.PARTIAL_EXPUNGEMENT
                conclusion.value.append(exp)
            if len(not_expungeable_case.charges) > 0:
                case_d.value = False
        
        remaining_recordord.cases.append(not_expungeable_case)
        conclusion.reasoning.append(case_d)

    else:
        # The global requirements for expunging anything on this record weren't met, so nothing can be 
        # expunged.
        remaining_recordord.cases = crecord.cases
    return remaining_recordord, conclusion 


def expunge_nonconvictions(crecord: CRecord) -> Tuple[CRecord, dict]:
    """
    18 Pa.C.S. 9122(a) provides that non-convictions (cases are closed with no disposition recorded) "shall be expunged."
    
    Returns:
        a Decision with:
            name: str,
            value: [Petition],
            reasoning: [Decision]
    """
    conclusion = Decision(
        name="Expungements of nonconvictions.",
        value=[],
        reasoning=[]
    )

    remaining_recordord = CRecord(person=crecord.person)
    for case in crecord.cases:
        case_d = Decision(
            name=f"Does {case.docket_number} have expungeable nonconvictions?",
            reasoning=[]
        )
        unexpungeable_case = case.partialcopy()
        expungeable_case = case.partialcopy()
        for charge in case.charges:
            charge_d = Decision(
                name=f"Is the charge for {charge.offense} a nonconviction?",
                value=not charge.is_conviction(),
                reasoning=f"The charge's disposition {charge.disposition} indicates a conviction" if charge.is_conviction() else f"The charge's disposition {charge.disposition} indicates its not a conviction."
            )

            if bool(charge_d) is True:
                expungeable_case.charges.append(charge)
            else:
                unexpungeable_case.charges.append(charge)
            case_d.reasoning.append(charge_d)

        # If there are any expungeable charges, add an Expungepent to the Value of the decision about
        # this whole record.
        if len(expungeable_case.charges) > 0:
            case_d.value = True
            exp = Expungement(client=crecord.person, cases=[expungeable_case])
            if len(expungeable_case.charges) == len(case.charges):
                exp.expungement_type = Expungement.ExpungementTypes.FULL_EXPUNGEMENT
            else:
                exp.expungement_type = Expungement.ExpungementTypes.PARTIAL_EXPUNGEMENT
            conclusion.value.append(exp)
        else:
            case_d.value = False

        if len(unexpungeable_case.charges) > 0:
            remaining_recordord.cases.append(unexpungeable_case)
        conclusion.reasoning.append(case_d)


    return remaining_recordord, conclusion 
