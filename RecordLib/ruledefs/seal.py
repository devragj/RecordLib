from __future__ import annotations
from RecordLib.crecord import CRecord, Charge
from typing import Tuple, Union, List
import copy
import json
import re
from RecordLib.decision import Decision
from RecordLib.petitions import Sealing


def no_danger_to_person_offense(
    item: Union[CRecord, Charge],
    within_years: int,
    penalty_limit: int,
    conviction_limit: int,
) -> Decision:
    """
    Individual is not eligible for sealing if they have been convicted within 20 years of an offense
    punishable by imprisonment of seven or more years which is an offense under Article B of Part II.
    
    18 Pa.C.S. 9122.1(b)(2)(A)(I) 


    A charge is not eligible for sealing if it is a conviction for an Article B of Part II (danger to the person)

    TODO currently sealing functions don't evaluate the time requirements (penalty_limit or within_years). B/C charges don't know when they happened.

    Args:
        item: A criminal record or a single Charge
        within_years: Person cannot have been convicted of the relevant offense within this number of years..
        penalty_limit: This rule applies to offenses with a sentence equal or greater than this limit.
        conviction_limit: The max number of times a peron can have this conviction before failing the rule.
    """
    # Suppose `item` is a whole Record.
    try:
        decision = Decision(
            name="No convictions in the record for article B offenses, felonies or punishable by more than 7 years, in the last 20 years.",
            reasoning=[no_danger_to_person_offense(charge, within_years=within_years, penalty_limit=penalty_limit, conviction_limit=conviction_limit)  for case in item.cases for charge in case.charges]
        )
        decision.value=all(decision.reasoning)
    except AttributeError:
        # `item` is probably a charge.
        decision = Decision(name="Is this not a conviction for an Article B offense")
        try:
            if (item.get_statute_chapter() == 18 and
                    item.get_statute_section() > 2300 and
                    item.get_statute_section() < 3300 and
                    item.is_conviction()):
                decision.value=False
                decision.reasoning=f"Statute {item.statute} is an Article B conviction"
            else:
                decison.value=True
                decison.reasoning=f"Statute {item.statute} appears not to be an Article B conviction."
        except:
            decision.value=True
            decision.reasoning=f"Couldn't read the statute {item.statute}, so its probably not Article B."

    return decision


def ten_years_since_last_conviction(crecord: CRecord) -> Decision:
    """
    Person is not eligible for sealing unless they have been "free from conviction
    for a period of 10 years" 18 Pa C.S. § 9122.1(a)

    Args:
        crecord: A criminal record

    Returns:
        a Decision indicating if the record has a conviction that's more recent than 10 years.
    """

    decision = Decision(
        name="Has the person been free of conviction for at least 10 years?",
        reasoning= [
            charge.is_conviction() and (case.years_passed_disposition() >= 10) for case in crecord.cases for charge in case.charges
    ])
    decision.value = all(decision.reasoning)
    

    return decision


def fines_and_costs_paid(crecord) -> Decision:
    """
    In individual is not eligible for sealing unless all fines and costs have been paid.

    18 Pa. C.S. § 9122.1(a).

    Args:
        crecord: A criminal record

    Returns:
        a Decision indicating if all fines and costs have been paid on the Record.
    """
    decision = Decision(
        name="Fines and costs are all paid on the whole record?",
        reasoning=[
            {"case": case.docket_number, "total fines": case.total_fines, "fines paid": case.fines_paid}
            for case in crecord.cases
        ],
    )
    try:
        # if the fines remaining for the record are less than 0, then this test passes.
        decision.value = sum([(case.fines_remaining()) for case in crecord.cases]) <= 0
    except TypeError:
        # If fines_and_costs is unknown for a case, the test above will fail,
        # and  we'll conservatively assume the worst, that there are unpaid fines and costs.
        decision.value = False
    return decision


def not_felony1(charge: Charge) -> Decision:
    """
    Any F1 graded offense disqualifies a whole record from sealing. 18 PA Code 9122.1(b)(2)(i)

    Returns:
        a True decision if the charge was NOT a felony1 conviction.
    """
    decision = Decision(name="Is the charge an F1 conviction?")
    if charge.grade.strip() == "":
        decision.value = False
        decision.reasoning = (
            "The charge's grade is unknown, so we don't know its *not* an F1."
        )
    elif re.match("F1", charge.grade):
        if charge.is_conviction():
            decision.value = False
            decision.reasoning = "The charge is an F1 conviction"
        else:
            decision.value = True
            decision.reasoning = (
                f"The charge was F1, but the disposition was {charge.disposition}"
            )
    else:
        decision.value = True
        decision.reasoning = f"The charge is {charge.grade}, which is not F1"

    return decision


def not_murder(charge: Charge) -> Decision:
    """
    Checks if a charge was a conviction for murder. 
    
    Returns:
         true if the charge was NOT a murder conviction.

    TODO The Expungement Generator's test is for the statute 18 PaCS 1502. Does the implementation here even work? Need to find real murder convictions to see.
    """
    decision = Decision(name="Is the charge NOT a murder conviction?")
    if charge.is_conviction():
        if re.match("murder", charge.offense, re.IGNORECASE):
            decision.value = False
            decision.reasoning = "The charge was a murder conviction."
        else:
            decision.value = True
            decision.reasoning = "Conviction for something other than murder."
    else:
        decision.value = True
        decision.reasoning = "Not a conviction."
    return decision


def no_f1_convictions(crecord: CRecord) -> Decision:
    """
    Any conviction for Murder, any F1 conviction, or any conviction punishable by imprisonment of 
    more than 20 years disqualifies a record from sealing.

    18 Pa.C.S. 9122.1(b)(2)(i)

    This method only checks for F1 and murder convictions, 
    not for convictions punishable by more than 20 years which are not F1 or murder.

    Returns:
        True if the charge is not a disqualifying conviction.
    """
    decision = Decision(name="No F1 or murder convictions in the record?")
    decision.reasoning = [
        not_felony1(charge) and not_murder(charge)
        for case in crecord.cases
        for charge in case.charges
    ]
    decision.value = all(decision.reasoning)
    return decision


def is_misdemeanor_or_ungraded(charge: Charge) -> Decision:
    """
    Sealing only available for 'qualifying misdemeanor or an ungraded offense which 
    carries a maximum penalty of no more than five years'. Pa.C.S. 9122.1(a).

    This only really checks if the offense was an M or ungraded. It doesn't know the maximum 
    penalty of an offense.

    Returns:
        True if the charge is not a disqualifying conviction.
    """
    decision = Decision(
        name="The offense is a misdemeanor or nongraded offense w/ a penalty of <= 5 years."
    )
    if re.match("^M", charge.grade):
        decision.reasoning = "Charge is a misdemeanor"
        decision.value = True
    elif charge.grade.strip() == "":
        decision.reasoning = "Charge is ungraded. But be careful - we don't know the maximum penalty for the offense."
        decision.value = True
    else:
        decision.reasoning = "Charge is neither a misdemeanor nor ungraded."
        decision.value = False
    return decision



def no_offense_against_family(
    item: Union[CRecord, Charge],
    penalty_limit: int,
    conviction_limit: int,
    within_years: int,
) -> Decision:
    """
    Individuals are ineligible for sealing with certain offenses against the family. (Article D of Part II)

    Individual ineligible after 1 conviction within 20 years of an offense against the family 
    if a felony or if punishable by seven or more years.  18 Pa.C.S. 9122.1(b)(2)(A).

    Individuals ineligible after 2 convictions within 15 years of an offense against the family 
    if a felony or punishable by more than 2 years. 18 Pa.C.S. 9122.1(b)(3)(ii)(B)

    Returns:
        True if the charge was NOT a disqualifying offense, or if the record does NOT contain any 
        disqulifying offenses.
    """
    # Presume a Charge
    try:
        decision = Decision(
            name=f"Charge for {item.statute} is not an offense against the family.",
            reasoning=[
                item.is_conviction(), 
                item.get_statute_chapter() == 18, 
                item.get_statute_section() > 4300,
                item.get_statute_section() < 4500
            ])
        decision.value = not all(decision.reasoning)
    except TypeError:
        # `item`'s get_statute functions returned something that doesn't have < > defined, such as None.
        decision = Decision(
            name=f"Charge for {item.statute} is not an offense against the family.",
            reasoning = "The statute doesn't appear to be one of the Article D offense statutes.",
            value=True
        )
    except AttributeError:
        # `item` may be a whole record.
        decision = Decision(
            name=(f"Not convicted within {within_years} more than {conviction_limit} times " +
                  f"of felony or offense punishable by {penalty_limit} years."),
            # reasoning should be a list of charges w/in 20 years where no_offense_fam(charge) is False
            reasoning = [no_offense_against_family(charge, penalty_limit=penalty_limit, conviction_limit=conviction_limit, within_years=within_years)
                         for case in item.cases for charge in case.charges
                         if case.years_passed_disposition() <= within_years]
        )
        decision.value = len(list(filter(lambda d: bool(d) is False, decision.reasoning))) < conviction_limit
    return decision



def no_firearms_offense(
    item: Union[CRecord, Charge],
    penalty_limit: int,
    conviction_limit: int,
    within_years: int,
) -> Decision:
    """
    No disqualifying convictions for firearms offenses. (Chapter 61 offenses) 
    
    No sealing conviction if punishable by more than two years for Chapter 61 (firearms) offenses. 
    18 Pa.C.S. 9122.1(b)(1)(iii)

    No sealing record if contains any conviction ithin 20 years for a felony or offense 
    punishable >= 7 years for Chapter 61 offenses. 18 Pa.C.S. 9122.1(b)(2)(ii)(A)(II)

    Returns:
        True if the charge was NOT a disqualifying offense, or if the record does NOT contain any 
        disqulifying offenses.
 
    """
    # assume item is a charge.
    try:
        decision = Decision(
            name=f"Charge for {item.statute} is not a firearms offense.",
            reasoning=[
                item.get_statute_chapter() == 18, 
                item.get_statute_section() > 6100,
                item.get_statute_section() < 6200
            ])
        decision.value = not all(decision.reasoning)
    except TypeError:
        # `item`'s get_statute functions returned something that doesn't have < > defined, such as None.
        decision = Decision(
            name=f"Charge for {item.statute} is not a Chapter 61 firearms offense.",
            reasoning = "The statute doesn't appear to be one of the Article D offense statutes.",
            value=True
        )
    except AttributeError:
        # `item` may be a whole record.
        decision = Decision(
            name=(f"Not convicted within {within_years} more than {conviction_limit} times " +
                  f"of felony or offense punishable by {penalty_limit} years."),
            # reasoning should be a list of charges w/in 20 years where no_offense_fam(charge) is False
            reasoning = [no_firearms_offense(charge, penalty_limit=penalty_limit, conviction_limit=conviction_limit, within_years=within_years)
                         for case in item.cases for charge in case.charges
                         if case.years_passed_disposition() <= within_years]
        )
        decision.value = len(list(filter(lambda d: bool(d) is False, decision.reasoning))) < conviction_limit
    return decision


def no_sexual_offense(
    item: Union[CRecord, Charge],
    penalty_limit: int,
    conviction_limit: int,
    within_years: int,
) -> Decision:
    """
    No disqualifying convictions for sexual offenses.

    No sealing a conviction if it was punishable by more than two years for offenses under 
    42 Pa.C.S. §§ 9799.14 (relating to sexual offenses and tier system) and 
    9799.55 (relating to registration). 18 Pa.C.S. 9122.1(b)(1)(iv)

    No sealing a record if it contains any conviction within 20 years for a felony or 
    offense punishable >= 7 years, for offenses under 42 Pa.C.S. §§ 9799.14 (relating to sexual 
    offenses and tier system) and 9799.55 (relating to registration). 18 PaCS 9122.1(b)(2)(ii)(A)(IV)

    Returns:
        True if the charge was NOT a disqualifying offense, or if the record does NOT contain any 
        disqulifying offenses.
    """
    # 18 Pa.C.S. 9799.14 and 9799.55 relate to quite a few other offenses.
    tiered_sex_offenses = ["2901a.1", "2902b",
					"2903b", "2904", "2910b", "3011b", "3121", "3122.1b", "3123",
					"3124.1", "3124.2a", "3124.2a.1", "3124.2a2", "3124.2a3",
					"3125", "3126a1", "3126a2", "3126a3", "3126a4", "3126a5",
					"3126a6", "3126a7", "3126a8", "4302b", "5902b", "5902b.1",
					"5903a3ii", "5903a4ii", "5903a5ii", "5903a6", "6301a1ii",
                    "6312", "6318", "6320", "7507.1"]
    # presume item is a Charge
    try:
        decision = Decision(name="This charge is not a disqualifying sexual or registration offense?")
        patt = re.compile(r"^(?P<chapt>\d+)\s*§\s(?P<section>\d+\.?\d*)\s*(?P<subsections>[\(\)A-Za-z0-9\.]+).*")
        matches = patt.match(item.statute)
        if not matches:
            decision.reasoning = "This doesn't appear to be one of the tiered sex offense statutes."
            decision.value = True
        else:
            this_offense = matches.group("section") + matches.group("subsections").replace("(","").replace(")","")
            decision.reasoning = [item.is_conviction(), 
                                  item.get_statute_chapter() == 18,
                                  this_offense in tiered_sex_offenses]
            decision.value = not all(decision.reasoning)
    except AttributeError: 
        # item is a CRecord
        decision = Decision(
            name=(f"Not convicted within {within_years} more than {conviction_limit} times " +
                  f"of certain sexual or registration-related offenses punishable by {penalty_limit} years"),
            reasoning = [no_sexual_offense(charge, penalty_limit=penalty_limit, conviction_limit=conviction_limit, within_years=within_years)
                         for case in item.cases for charge in case.charges
                         if case.years_passed_disposition() <= within_years]
        )
        decision.value = len(list(filter(lambda d: bool(d) is False, decision.reasoning))) < conviction_limit
    return decision


def no_corruption_of_minors_offense(
    charge: Charge, penalty_limit: int, conviction_limit: int, within_years: int
) -> Decision:
    """
    No disqualifying convictions for corruption of minors.

    No sealing a conviction if it was punishable by more than two years for offenses under 
    section 6301(a)(1), corruption of minors. 18 Pa.C.S. 9122.1(b)(1)(v)

    Returns:
        a True Decision if the charge was NOT a disqualifying offense. Otherwise a False Decision.
    """
    decision = Decision(name="This charge is not a disqualifying corruption of minors offense?")
    patt = re.compile(r"^(?P<chapt>\d+)\s*§\s(?P<section>\d+\.?\d*)\s*(?P<subsections>[\(\)A-Za-z0-9\.]+).*")
    matches = patt.match(charge.statute)
    if not matches:
        decision.reasoning = "This doesn't appear to be one of the tiered sex offense statutes."
        decision.value = True
    else:
        this_offense = matches.group("section") + matches.group("subsections").replace("(","").replace(")","")
        decision.reasoning = [charge.is_conviction(), 
                                charge.get_statute_chapter() == 18,
                                this_offense == "6301a1"]
        decision.value = not all(decision.reasoning)
    return decision


def offenses_punishable_by_two_or_more_years(
    crecord: CRecord, conviction_limit: int, within_years: int
) -> Decision:
    """
    Not too many convictions for offenses punishable by two or more years.
    
    No sealing a record if it has four or more offenses punishable by two or more years within 20 years. 
    18 PaCS 9122.1(b)(2)(ii)(B)
    
    No sealing a record if it has two or more offenses punishable by more than two years in prison within
    15 years.. 18 PaCS 9122.1(b)(2)(iii)(A)

    The Expungement Generator uses the charge grade as a proxy for this. See Charge.php:284.

    So will RecordLib.

    Returns:
        A Decision we'll call `d`. `bool(d)` is True if there were no offenses punishable by more than 
        two years in `crecord`.

    """
    # Grades that approximately the grades of offenses that also have penalty's of two or more years.
    proxy_grades = ["F1", "F2", "F3", "F", "M1", "M2"]
    decision = Decision(
        name=f"The record has no more than {conviction_limit} convictions for offenses punishable by two or more years in the last {within_years} years.",
        reasoning=[
            charge for case in crecord.cases for charge in case.charges 
                if (charge.is_conviction() and 
                    (charge.grade in proxy_grades) and 
                    case.years_passed_disposition() < within_years)
        ]
    )
    decision.value = len(decision.reasoning) < conviction_limit

    return decision


def no_indecent_exposure(crecord, conviction_limit: int, within_years: int=15) -> Decision:
    """
    Cannot seal if record contains conviction for indecent exposure within 15 years.
    18 PaCS 9122.1(b)(2)(iii)(B)(I)
    
    Returns:
        A Decision we'll call `d`. `bool(d)` is True if there were no indecent exposure 
        offenses in `crecord`.

    """
    decision = Decision(
        name="No indecent exposure convictions in this record.",
        reasoning=[charge for case in crecord.cases for charge in case.charges if 
            (case.years_passed_disposition() < within_years and
                        charge.is_conviction() and 
                        charge.get_statute_chapter() == 18 and
                        charge.get_statute_section() == 3127)]
    )
    decision.value = True if len(decision.reasoning) < conviction_limit else False
    return decision



def no_sexual_intercourse_w_animal(
    crecord: CRecord, conviction_limit: int, within_years: int=15) -> Decision:
    """
    Cannot seal if record contains conviction for intercourse w/ animal within 15 years.

    18 PA.C.S. 9122.1(b)(2)(iii)(B)(II)
    
    Returns:
        Decision that is True if there were no sexual intercourse w/ animal convictions in the record.  
    """
    decision = Decision(
        name="No intercourse with animals convictions in this record.",
        reasoning=[charge for case in crecord.cases for charge in case.charges if 
                       (case.years_passed_disposition() < within_years and
                        charge.is_conviction() and 
                        charge.get_statute_chapter() == 18 and
                        charge.get_statute_section() == 3129)]
    )
    decision.value = True if len(decision.reasoning) < conviction_limit else False
    return decision


def no_failure_to_register(
    crecord: CRecord, conviction_limit: int, within_years: int=15) -> Decision:
    """
    Cannot seal if record contains conviction for failure to register within 15 years.

    18 PA.C.S. 9122.1(b)(2)(iii)(B)(III)

    Returns:
        a Decision that is True if there were no failure-to-register offenses in the record.
    """
    decision = Decision(
        name="No failure-to-register convictions in this record.",
        reasoning=[charge for case in crecord.cases for charge in case.charges if 
                       (case.years_passed_disposition() < within_years and
                        charge.is_conviction() and 
                        charge.get_statute_chapter() == 18 and
                        (charge.get_statute_section() == 4915.1 or
                         charge.get_statute_section() == 4915.2))]
    )
    decision.value = True if len(decision.reasoning) < conviction_limit else False
    return decision


def no_weapons_of_escape(
    crecord: CRecord, conviction_limit: int, within_years: int=15) -> Decision:
    """
    Cannot seal if record contains conviction for possession of implement or weapon of escape within 15 years.

    18 PA.C.S. 9122.1(b)(2)(iii)(B)(IV)
    """
    decision = Decision(
        name="No possion-of-implement-of-escape convictions in this record.",
        reasoning=[charge for case in crecord.cases for charge in case.charges if 
                       (case.years_passed_disposition() < within_years and
                        charge.is_conviction() and 
                        charge.get_statute_chapter() == 18 and
                        charge.get_statute_section() == 5122)]
    )
    decision.value = True if len(decision.reasoning) < conviction_limit else False
    return decision


def no_abuse_of_corpse(
    crecord: CRecord, conviction_limit: int, within_years: int=15
) -> Decision:
    """
    Cannot seal if record contains conviction for abuse of corpse within 15 years.

    18 PA.C.S. 9122.1(b)(2)(iii)(B)(V)
    """
    decision = Decision(
        name="No abuse of corpse convictions in this record.",
        reasoning = [charge for case in crecord.cases for charge in case.charges if 
                       (case.years_passed_disposition() < within_years and
                        charge.is_conviction() and 
                        charge.get_statute_chapter() == 18 and
                        charge.get_statute_section() == 5510)]
    )
    decision.value = True if len(decision.reasoning) < conviction_limit else False
    return decision



def no_paramilitary_training(
    crecord: CRecord, conviction_limit: int, within_years: int=15) -> Decision:
    """
    Cannot seal if record contains conviction for paramilitary training within 15 years.

    18 PA.C.S. 9122.1(b)(2)(iii)(B)(VI)
    """
    decision = Decision(
        name="No paramilitary training offenses in this record.",
        reasoning=[charge for case in crecord.cases for charge in case.charges if 
                       (case.years_passed_disposition() < within_years and
                        charge.is_conviction() and 
                        charge.get_statute_chapter() == 18 and
                        charge.get_statute_section() == 5515)]
    )
    decision.value = True if len(decision.reasoning) < conviction_limit else False
    return decision

def seal_convictions(crecord: CRecord) -> Tuple[CRecord, Decision]:
    """
    Pa.C.S. 9122.1 provides for petition-based sealing of records when certain
    conditions are met.

    Paragraph (a) provides a general rule that sealing is available when someone has been free of conviction for 10 years of certain offenses, and has paid fines and costs.


    Returns:
        A Decision. The decision's name is "Sealable Convictions". Its `value` is a list of the Cases and 
            charges that are selable from `crecord`. 
            Its `reasoning` is a list of all the decisions relating to the whole record, and all the decisions 
            relating to each case.

    TODO Paragraph (b)(2) provides conditions that disqualify a person's whole record from sealing.

    TODO Paragraph (b)(1) provides conditions that exclude convictions from sealing.
    """
    conclusion = Decision(
        name="Convictions can be sealed under the Clean Slate reforms.",
        value=[])
    mod_rec = CRecord(person=crecord.person, cases=[])

    # Requirements for sealing any part of a record
    conclusion.reasoning = [
        ten_years_since_last_conviction(crecord),  # 18 Pa.C.S. 9122.1(a)
        fines_and_costs_paid(crecord),  # 18 Pa.C.S. 9122.1(a)
        no_f1_convictions(crecord),  # 18 Pa.C.S. 9122.1(b)(2)(i)
        no_danger_to_person_offense(
            crecord, penalty_limit=7, conviction_limit=1, within_years=20
        ),
        no_offense_against_family(
            crecord, penalty_limit=7, conviction_limit=1, within_years=20
        ),
        no_firearms_offense(
            crecord, penalty_limit=7, conviction_limit=1, within_years=20
        ),
        no_sexual_offense(
            crecord, penalty_limit=7, conviction_limit=1, within_years=20
        ),
        offenses_punishable_by_two_or_more_years(
            crecord, conviction_limit=4, within_years=20
        ),
        offenses_punishable_by_two_or_more_years(
            crecord, conviction_limit=2, within_years=15
        ),
        no_indecent_exposure(crecord, conviction_limit=1, within_years=15),
        no_sexual_intercourse_w_animal(crecord, conviction_limit=1, within_years=15),
        no_failure_to_register(crecord, conviction_limit=1, within_years=15),
        no_weapons_of_escape(crecord, conviction_limit=1, within_years=15),
        no_abuse_of_corpse(crecord, conviction_limit=1, within_years=15),
        no_paramilitary_training(crecord, conviction_limit=1, within_years=15),
    ]
    if all(conclusion.reasoning):
        for case in crecord.cases:
            # The sealability of each case is its own decision
            case_decision = Decision(
                name=f"Sealing case {case.docket_number}", reasoning=[]
            )
            # create copies of a case that don't include any charges.
            # sealable or unsealable charges will be added to these.
            sealable_parts_of_case = case.partialcopy()
            unsealable_parts_of_case = case.partialcopy()
            for charge in case.charges:
                # The sealability of each charge is its own Decision.
                charge_decision = Decision(name=f"Sealing charge {charge.offense}")
                # Conditions that determine whether this charge is sealable
                #  See 91 Pa.C.S. 9122.1(b)(1)
                charge_decision.reasoning = [
                    charge.set_grade(),
                    is_misdemeanor_or_ungraded(charge),
                    no_danger_to_person_offense(
                        charge,
                        penalty_limit=2,
                        conviction_limit=1,
                        within_years=float("Inf"),
                    ),
                    no_offense_against_family(
                        charge,
                        penalty_limit=2,
                        conviction_limit=1,
                        within_years=float("Inf"),
                    ),
                    no_firearms_offense(
                        charge,
                        penalty_limit=2,
                        conviction_limit=1,
                        within_years=float("Inf"),
                    ),
                    no_sexual_offense(
                        charge,
                        penalty_limit=2,
                        conviction_limit=1,
                        within_years=float("Inf"),
                    ),
                    no_corruption_of_minors_offense(
                        charge,
                        penalty_limit=2,
                        conviction_limit=1,
                        within_years=float("Inf"),
                    ),
                ]
                if all(charge_decision.reasoning):
                    charge_decision.value = "Sealable"
                    sealable_parts_of_case.charges.append(charge)
                    # N.B. Appending charge, not deepcopy(charge), because I don't think
                    # the overhead is neccessary. But that could turn out to be wrong someday.
                else:
                    charge_decision.value = "Not sealable"
                    unsealable_parts_of_case.charges.append(charge)
                case_decision.reasoning.append(charge_decision)
            if all([reason.value == "Sealable" for reason in case_decision.reasoning]):
                # All the charges in the current case are sealable.
                case_decision.value = "All charges sealable"
                conclusion.value.append(Sealing(client=crecord.person, cases=[sealable_parts_of_case]))
            elif any(
                [reason.value == "Sealable" for reason in case_decision.reasoning]
            ):
                # At least one charge in the current case is sealable.
                case_decision.value = "Some charges sealable"
                mod_rec.cases.append(unsealable_parts_of_case)
                conclusion.value.append(Sealing(client=crecord.person, cases=[sealable_parts_of_case]))
            else:
                case_decision.value = "No charges sealable"
                mod_rec.cases.append(unsealable_parts_of_case)
            conclusion.reasoning.append(case_decision)

    return mod_rec, conclusion
