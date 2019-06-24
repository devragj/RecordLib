"""
Collect rule-functions that take a record and return an analysis of
how the rule applies to the record.
"""
from RecordLib.crecord import CRecord

## 18 PA 9122 Expungements
## https://www.legis.state.pa.us/cfdocs/legis/LI/consCheck.cfm?txtType=HTM&ttl=18&div=0&chpt=91


def expunge_over_70(crecord: CRecord) -> dict:
    """
    Analyze a crecord for expungements if the defendant is over 70.

    18 PA 9122(b)(1) provides for expungements of an individual who
    is 70 or older, and has been free of arrest or prosecution for 10
    years following the final release from confinement or supervision.
    """

    if ((crecord.person.age() > 70) and
        (crecord.years_since_last_arrested_or_prosecuted() > 10) and
        (crecord.years_since_final_release() > 10)):
            return crecord, {"expunge_over_70": crecord.cases}
    return crecord, {"expunge_over_70": []}


def expunge_deceased(crecord: CRecord) -> dict:
    """
    Analyze a crecord for expungments if the individual has been dead for three years.

    18 PA 9122(b)(2) provides for expungement of records for an individual who has been dead for three years.
    """
    pass


def expunge_summaries(crecord: CRecord) -> dict:
    """
    Analyze crecord for expungements of summary convictions.

    18 PA 9122(b)(3)(i) and (ii) provide for expungement of summary convictions if the individual has been free of arrest or prosecution for five years following the conviction for the offense.

    Not available if person got ARD for certain offenses listed in (b.1)
    """
    pass


rules = [
    expunge_over_70,
    expunge_deceased
]
