"""
Module for tools to remove overflowing lines from dockets.


Lines that repeat across page breaks in summaries and dockets are a big problem. These tools deal with those.
"""
from typing import List, Tuple
import re
import pytest
from RecordLib.references import pa_counties, statuses

class OverflowFilter:
    @staticmethod
    def condition(prev: List[str], next: List[str]) -> bool:
        """ True or false, depending on whether this class's condition is satisfied.

        """
        raise NotImplementedError

    @staticmethod
    def remove_overflow(prev: List[str], next: List[str]) -> Tuple[List[str],List[str]]:
        """ Remove the overflow lines from two lists of strings.
        """
        raise NotImplementedError

    @staticmethod
    def previous_nonblank_line(prev: List[str], n=1) -> str:
        """Return the nth nonblank line fron the end of a list of lines.

        Args:
            prev: list of lines
            n: return the nth nonblank line. If n is 1, return the last nonblank line. If n is 2, return the second nonblank line from the end of `prev`. Etc.
        """
        counter = 1
        for ln in reversed(prev):
            if ln.strip() != "":
                if n==counter:
                    return ln
                else:
                    counter += 1
        return ""

class MDJOverflowInChargeList(OverflowFilter):
    """Overflow filter for MDJ Summary sheets, in the case where a page overflows in the middle of a list of charges."""
    @staticmethod
    def condition(prev: List[str], next: List[str]) -> bool:
        if re.search("§", OverflowFilter.previous_nonblank_line(prev)) and re.search("Statute", next[2]):
            return True
        if re.search("§", OverflowFilter.previous_nonblank_line(prev, n=2)) and re.search("Statute", next[2]):
            return True
        if re.search("§", OverflowFilter.previous_nonblank_line(prev, n=2)) and re.search("Program", next[3]):
            return True
        if re.search("§", OverflowFilter.previous_nonblank_line(prev)) and re.search("Statewide", next[0]) and re.search("Statute", next[3]):
            return True
        if re.search("§", OverflowFilter.previous_nonblank_line(prev, n=2)) and re.search("Statewide", next[0]) and re.search("Statute", next[3]):
            return True
        return False


    @staticmethod
    def remove_overflow(prev: List[str], next: List[str]) -> Tuple[List[str],List[str]]:
        while prev and prev[-1].strip() == "": prev.pop()
        if re.search("Program", next[3]):
            # There should be a blank line before Program.
            next = next[2:]
        elif re.search("Statewide", next[0]):
            next = next[4:]
        else:
            next = next[3:]
        return prev, next



class MDJFirstCoupleLinesOverflow(OverflowFilter):
    """ Overflow filter for MDJ summary sheets, in the case where just the first couple lines of a case_category overlow.

    For example:

    [prev section]
    Inactive
       Erie


    <EOF>

    [next section]
    Statewide
    Inactive
        Erie
        MJ-<...>
    """
    def condition(prev: List[str], next: List[str]) -> bool:
        """ True or false, depending on whether this class's condition is satisfied.

        True if the page overflows after just the case status and a county name.
        """
        preceeding_blanks = 0
        for ln in reversed(prev):
            if ln.strip() != "":
                prev_nonblank_line = ln
                break
            preceeding_blanks += 1
        if re.search("|".join(pa_counties) + "|" + "|".join(statuses),prev_nonblank_line):
            return True

    def remove_overflow(prev: List[str], next: List[str]) -> Tuple[List[str],List[str]]:
        already_found_text = False
        lines_to_remove = 0
        for ln in reversed(prev):
            if ln.strip() != "":
                already_found_text = True
            elif ln.strip() == "" and already_found_text == True:
                break
            lines_to_remove += 1
        if lines_to_remove > 0:
            return prev[:-lines_to_remove], next
        return prev, next
