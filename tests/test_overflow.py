from RecordLib.overflow import (
    MDJFirstCoupleLinesOverflow,
    MDJOverflowInChargeList,
    OverflowFilter
)
import pytest
import re

def test_previous_nonblank_line():
    ls = ["1","2","3"," "]
    assert OverflowFilter.previous_nonblank_line(ls) == "3"
    assert OverflowFilter.previous_nonblank_line(ls, n=2) == "2"


def test_MDJOverflowInChargeListWithSentence():
    prev = \
"""       18 § 5505                          S           Public Drunkenness And Similar                       Guilty Plea                                    1
                                                      Misconduct

""".split("\n")
    next = \
"""County: Cambria
 Closed

       Program Type                                 Sentence Date                        Sentence Length                                   Program Period
       Community Service                            02/21/2018
""".split("\n")
    assert MDJOverflowInChargeList.condition(prev, next) is True
    prev, nxt = MDJOverflowInChargeList.remove_overflow(prev, next)
    assert re.search("Program", nxt[1])


def test_MDJOverflowInChargeList():

    prev = \
"""35 § 780-113 §§ A30       F   Mfr With     Waived for Court    1
                      Intent to Manufacture or Deliver

""".split("\n")

    next = \
"""County: Westmoreland
  Closed
       Statute          Grade       Description   Disposition      Counts
       35 § 780-113 §§ A31I         M           MJ Use   Waived for Court    1

""".split("\n")


    assert MDJOverflowInChargeList.condition(prev, next) is True
    prev, nxt = MDJOverflowInChargeList.remove_overflow(prev, next)
    assert re.search("35 § 780", nxt[0])

def test_MDJOverflowInChargeListWithStatewide():
    prev = \
"""35 § 780-113 §§ A30       F   Mfr With     Waived for Court    1
                      Intent to Manufacture or Deliver

""".split("\n")

    next = \
"""Statewide
    Closed
       County: Westmoreland
       Statute          Grade       Description   Disposition      Counts
       35 § 780-113 §§ A31I         M           MJ Use   Waived for Court    1

""".split("\n")

    assert MDJOverflowInChargeList.condition(prev, next) is True
    prev, nxt = MDJOverflowInChargeList.remove_overflow(prev, next)
    assert re.search("35 § 780", nxt[0])

def test_MDJFirstCoupleLinesOverflow():
    prev = \
    """

    County: Mercer
        Inactive


    """.split("\n")

    next = \
    """
    County: Mercer
    Inactive
        MJ-352
    """.split("\n")

    assert MDJFirstCoupleLinesOverflow.condition(prev, next) is True
    prev, next = MDJFirstCoupleLinesOverflow.remove_overflow(prev, next)
    assert "\n".join(prev) == "\n"

def test_MDJFirstCoupleLinesOverflowInStatewideSection():
    """ In a Statewide section, the status comes before the county. """

    prev = \
    """

    Inactive
        Mercer


    """.split("\n")

    next = \
    """
    Statewide
    Inactive
        Mercer
        MJ-352
    """.split("\n")

    assert MDJFirstCoupleLinesOverflow.condition(prev, next) is True
    prev, next = MDJFirstCoupleLinesOverflow.remove_overflow(prev, next)
    assert "\n".join(prev) == "\n"
