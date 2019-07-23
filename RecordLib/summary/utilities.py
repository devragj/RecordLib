import re
from lxml import etree
from datetime import datetime


def visit_sentence_length(self, node, vc):
    """
    Custom node visitor for parsing a setence in a conviction.

    returns an xml tree along the lines of
        <sentence_length>
            <min_length> <time> __ </time> <unit> __ </unit> </min_length>
            <max_length> <time> __ </time> <unit> __ </unit> </max_length>
        </sentence_length>
    """

    # Sentence lengths can appear in lots of formats, so this attempts to parse different
    # possibilities.
    min_pattern = re.compile(
        r".*(?:min of|Min:) (?P<time>[0-9\./]*) (?P<unit>\w+).*",
        flags=re.IGNORECASE | re.DOTALL,
    )
    max_pattern = re.compile(
        r".*(?:max of|Max:) (?P<time>[0-9\./]*) (?P<unit>\w+).*",
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Original from DocketParse
    # range_pattern = re.compile(r".*?(?P<min_time>(?:[0-9\.\/]+(?:\s|$))+)(?P<min_unit>\w+ )?(?:to|-)? (?P<max_time>(?:[0-9\.\/]+(?:\s|$))+)(?P<max_unit>\w+).*", flags=re.IGNORECASE|re.DOTALL)

    range_pattern = re.compile(
        r".*: (?P<min_time>[0-9\.\/]+) (?P<min_unit>\w+)?(?:to|-)?.*: (?P<max_time>[0-9\.\/]+) (?P<max_unit>\w+).*",
        flags=re.IGNORECASE | re.DOTALL,
    )

    single_term_pattern = re.compile(
        r".*\s{5,}(?P<time>[0-9\./]+)\s(?P<unit>\w+)$.*",
        flags=re.IGNORECASE | re.DOTALL,
    )
    # temp_string = node.text
    #    print(temp_string)
    min_length = None
    max_length = None
    min_length_match = re.match(min_pattern, node.text)
    max_length_match = re.match(max_pattern, node.text)
    range = re.match(range_pattern, node.text)
    single_term = re.match(single_term_pattern, node.text)

    if min_length_match is not None:
        min_length = (
            f"<min_length> <time> {min_length_match.group('time')} </time> "
            + f"<unit> {min_length_match.group('unit')} </unit> </min_length>"
        )
        if max_length_match is None:
            max_length = (
                f"<max_length> <time> {min_length_match.group('time')} </time> "
                + f" <unit> {min_length_match.group('unit')} </unit> </max_length>"
            )

    if max_length_match is not None:
        max_length = (
            "<max_length> <time> %s </time> <unit> %s </unit> </max_length>"
            % (max_length_match.group("time"), max_length_match.group("unit"))
        )
        if min_length_match is None:
            min_length = (
                "<min_length> <time> %s </time> <unit> %s </unit> </min_length>"
                % (max_length_match.group("time"), max_length_match.group("unit"))
            )

    if range is not None:
        if range.group("min_unit") is not None:
            min_length = (
                "<min_length> <time> %s </time> <unit> %s </unit> </min_length>"
                % (range.group("min_time"), range.group("min_unit"))
            )
        else:
            min_length = (
                "<min_length> <time> %s </time> <unit> %s </unit> </min_length>"
                % (range.group("min_time"), range.group("max_unit"))
            )
        max_length = (
            "<max_length> <time> %s </time> <unit> %s </unit> </max_length>"
            % (range.group("max_time"), range.group("max_unit"))
        )

    if single_term is not None:
        min_length = (
            "<min_length> <time> %s </time> <unit> %s </unit> </min_length>"
            % (single_term.group("time"), single_term.group("unit"))
        )
        max_length = (
            "<max_length> <time> %s </time> <unit> %s </unit> </max_length>"
            % (single_term.group("time"), single_term.group("unit"))
        )

    contents = self.stringify(vc)
    if min_length is not None and max_length is not None:
        contents = min_length + " " + max_length

    return " <sentence_length> %s </sentence_length> " % contents


def text_or_blank(element: etree.Element) -> str:
    """
    Extract the text of an element, if any, or return a blank string.
    """
    try:
        return element.text.strip()
    except AttributeError:
        return ""


def date_or_none(date_element: etree.Element, fmtstr: str = "%m/%d/%Y") -> datetime:
    """
    Return date or None given a string.
    """
    try:
        return datetime.strptime(date_element.text.strip(), fmtstr).date()
    except (ValueError, AttributeError):
        return None
