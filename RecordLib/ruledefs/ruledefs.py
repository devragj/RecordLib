"""
Collect rule-functions that take a record and return an analysis of
how the rule applies to the record.

18 Pa.C.S. 9122 deals with Expungements
https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm?txtType=HTM&ttl=18&div=0&chpt=91
"""
from RecordLib.crecord import CRecord
import pytest
import copy
from typing import Tuple
from dateutil.relativedelta import relativedelta
from datetime import date
import re


def expunge_over_70(crecord: CRecord, analysis: dict) -> Tuple[CRecord, dict]:
    """
    Analyze a crecord for expungements if the defendant is over 70.

    18 Pa.C.S. 9122(b)(1) provides for expungements of an individual who
    is 70 or older, and has been free of arrest or prosecution for 10
    years following the final release from confinement or supervision.
    """
    conditions = {
        "age_over_70": crecord.person.age() > 70,
        "years_since_last_arrested_or_prosecuted": crecord.years_since_last_arrested_or_prosecuted()
        > 10,
        "years_since_final_release": crecord.years_since_final_release() > 10,
    }

    if all(conditions.values()):
        conclusion = "Expunge cases"
        modified_record = CRecord(person=copy.deepcopy(crecord.person), cases=[])
    else:
        conclusion = "No expungements possible"
        modified_record = crecord
    analysis.update(
        {
            "age_over_70_expungements": {
                "conditions": conditions,
                "conclusion": conclusion,
            }
        }
    )

    return modified_record, analysis


def expunge_deceased(crecord: CRecord, analysis: dict) -> Tuple[CRecord, dict]:
    """
    Analyze a crecord for expungments if the individual has been dead for three years.

    18 Pa.C.S. 9122(b)(2) provides for expungement of records for an individual who has been dead for three years.
    """
    conditions = {"deceased_three_years": crecord.person.years_dead() > 3}

    if all(conditions.values()):
        conclusion = "Expunge cases"
        modified_record = CRecord(person=copy.deepcopy(crecord.person), cases=[])
    else:
        conclusion = "No expungements possible"
        modified_record = crecord

    analysis.update(
        {"deceased_expungements": {"conditions": conditions, "conclusion": conclusion}}
    )

    return modified_record, analysis


def expunge_summary_convictions(
    crecord: CRecord, analysis: dict
) -> Tuple[CRecord, dict]:
    """
    Analyze crecord for expungements of summary convictions.

    18 Pa.C.S. 9122(b)(3)(i) and (ii) provide for expungement of summary convictions if the individual has been free of arrest or prosecution for five years following the conviction for the offense.

    Not available if person got ARD for certain offenses listed in (b.1)

    TODO excluding ARD offenses from expungements here.

    TODO grades are often missing. We should tell users we're uncertain.
    """
    conditions = {
        "arrest_free_five_years": crecord.years_since_last_arrested_or_prosecuted() > 5
    }
    expungements = []
    num_charges = 0
    num_expungeable_charges = 0
    modified_record = CRecord(person=crecord.person)
    for case in crecord.cases:
        any_expungements = False
        expungements_this_case = {"docket_number": case.docket_number}
        for charge in case.charges:
            num_charges += 1
            if charge.grade.strip() == "S":
                num_expungeable_charges += 1
                expungements_this_case.update({"charge": charge})
                any_expungements = True
        expungements.append(expungements_this_case)

        if any_expungements is False:
            modified_record.cases.append(copy.deepcopy(case))

    if (not all(conditions.values())) or num_expungeable_charges == 0:
        conclusion = "No expungements possible"
    elif all(conditions.values()) and num_charges == num_expungeable_charges:
        conclusion = "Expunge all cases"
    else:
        conclusion = (
            f"Expunge {num_expungeable_charges} charges in {len(crecord.cases)} cases"
        )

    analysis.update(
        {
            "summary_conviction_expungements": {
                "conditions": conditions,
                "conclusion": conclusion,
                "expungements": expungements if all(conditions.values()) else [],
            }
        }
    )

    return modified_record, analysis


def expunge_nonconvictions(crecord: CRecord, analysis: dict) -> Tuple[CRecord, dict]:
    """
    18 Pa.C.S. 9122(a) provides that non-convictions (cases are closed with no disposition recorded) "shall be expunged."
    """
    conditions = {"Nonconvictions can always be expunged.": True}
    expungements = []
    num_charges = 0
    num_expungeable_charges = 0
    modified_record = CRecord(person=crecord.person)
    if all(conditions.values()):
        for case in crecord.cases:
            unexpunged_case = copy.deepcopy(case)
            unexpunged_case.charges = []
            expungements_this_case = {
                "docket_number": case.docket_number,
                "charges": list()}
            for charge in case.charges:
                num_charges += 1
                if charge.disposition.strip() == "" or any(
                    [
                        re.match(disp, charge.disposition, re.IGNORECASE)
                        for disp in [
                            "Nolle Prossed",
                            "Withdrawn",
                            "Not Guilty",
                            "Dismissed",
                        ]
                    ]
                ):
                    num_expungeable_charges += 1
                    expungements_this_case["charges"].append(charge)
                else:
                    unexpunged_case.charges.append(charge)
            if len(expungements_this_case["charges"]) > 0:
                expungements.append(expungements_this_case)
            if len(expungements_this_case["charges"]) < len(case.charges):
                modified_record.cases.append(unexpunged_case)

    if num_expungeable_charges == 0:
        conclusion = "No expungements possible"
    elif num_charges == num_expungeable_charges:
        conclusion = "Expunge all cases"
    else:
        conclusion = "Expunge some cases"

    analysis.update(
        {
            "expunge_nonconvictions": {
                "conditions": conditions,
                "conclusion": conclusion,
                "expungements": expungements,
            }
        }
    )

    return modified_record, analysis
