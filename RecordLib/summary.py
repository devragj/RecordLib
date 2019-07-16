from __future__ import annotations
from typing import BinaryIO, Union, List
import io
import parsimonious  # type: ignore
from parsimonious.nodes import Node  # type: ignore
from RecordLib.grammars.summary import (
    summary_page_grammar,
    summary_page_terminals,
    summary_page_nonterminals,
    summary_body_grammar,
    summary_body_terminals,
    summary_body_nonterminals,
)
from RecordLib.CustomNodeVisitorFactory import CustomVisitorFactory
from RecordLib.case import Case
from RecordLib.common import Person, Charge, Sentence, SentenceLength
import pytest
import os
from lxml import etree
from collections import namedtuple
from datetime import datetime
import re
import logging


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
        ".*: (?P<min_time>[0-9\.\/]+) (?P<min_unit>\w+)?(?:to|-)?.*: (?P<max_time>[0-9\.\/]+) (?P<max_unit>\w+).*",
        flags=re.IGNORECASE | re.DOTALL,
    )

    single_term_pattern = re.compile(
        r".*\s{5,}(?P<time>[0-9\./]+)\s(?P<unit>\w+)$.*",
        flags=re.IGNORECASE | re.DOTALL,
    )
    temp_string = node.text
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


def date_or_none(date_element: etree.Element, fmtstr: str = "%m/%d/%Y") -> date:
    """
    Return date or None given a string.
    """
    try:
        return datetime.strptime(date_element.text.strip(), fmtstr).date()
    except (ValueError, AttributeError):
        return None


def parse_pdf(
    summary: Summary, pdf: Union[BinaryIO, str], tempdir: str = "tmp"
) -> Summary:
    """
    parse a pdf and store different information about the parsing in
    summary
    """
    if hasattr(pdf, "read"):
        # the pdf attribute is a file object,
        # and we need to write it out, for pdftotext to use it.
        pdf_path = os.path.join(tempdir, "tmp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf.read())
    else:
        pdf_path = pdf

    out_path = os.path.join(tempdir, "tmp.txt")
    os.system(f'pdftotext -layout -enc "UTF-8" { pdf_path } { out_path }')

    try:
        with open(os.path.join(tempdir, "tmp.txt"), "r") as f:
            summary.text = f.read()
    except:
        raise ValueError("Cannot extract summary text..")

    os.remove(os.path.join(tempdir, "tmp.txt"))
    slines = summary.text.split("\n")
    # Parse each page (a header, body, and footer)
    try:
        summary.parsed_pages = summary_page_grammar.parse(summary.text)
    except Exception as e:
        # pytest.set_trace()
        raise ValueError("Grammar cannot parse summary.")

    summary_page_visitor = CustomVisitorFactory(
        summary_page_terminals, summary_page_nonterminals, dict()
    ).create_instance()

    # the summary is now a string of xml along the lines of:
    # <summary> <first_page> ... </first_page>
    # <following_page> ... </following_page> </summary>\
    xml_parser = etree.XMLParser(encoding="UTF-8", recover=True)
    pages_xml_tree = etree.fromstring(
        summary_page_visitor.visit(summary.parsed_pages), xml_parser
    )

    # combine the body sections from each page and parse the combined body
    summary_info_sections = pages_xml_tree.findall(".//summary_info")

    ## Combine the text of the sections into one string
    ## When there's a page break over sections, then an empty line gets
    ## inserted, and I'd like to get rid of it, to help the grammars.
    logging.info(f"Page count: {len(summary_info_sections)}")
    for i, section in enumerate(summary_info_sections):
        if section.text[-2] == "\n" and section.text[-1] == " ":
            if i < (len(summary_info_sections) - 1):
                if "(Continued)" in summary_info_sections[i + 1].text[0:50]:
                    section.text = section.text[:-2]

    def find_in_lines(lines, id):
        for line in lines:
            if id in line:
                return True

        return False

    # Then split into lines, so we can remove lines that say (Continued) and other overflow lines.
    slines = []
    previous_sec_lines = []
    for i, sec in enumerate(summary_info_sections):
        sec_lines = sec.text.split("\n")
        line_count = len(sec_lines)
        lines_to_remove = 0
        if line_count > 0 and "(Continued)" in sec_lines[0]:
            lines_to_remove += 1
            if line_count > 1 and "(Continued)" in sec_lines[1]:
                lines_to_remove += 1
                if line_count > 2:
                    line = sec_lines[2]
                    pattern = '(CP\S+)\s'
                    match = re.search(pattern, line)
                    if match:
                        cp_id = match.group(1)
                        # print(cp_id)
                        if find_in_lines(previous_sec_lines, cp_id):
                            lines_to_remove += 1
                            if line_count > 3 and 'Arrest Dt' in sec_lines[3]:
                                lines_to_remove += 1
                                if line_count > 4 and 'Def Atty' in sec_lines[4]:
                                    lines_to_remove += 1
                                    if line_count > 5 and 'Seq No' in sec_lines[5]:
                                        lines_to_remove += 1
                                        if line_count > 6 and 'Sentence' in sec_lines[6]:
                                            lines_to_remove += 1
                            elif line_count > 3 and 'Seq No' in sec_lines[3]:
                                p_line = previous_sec_lines[-1]
                                test = 'Def' in p_line or 'Arrest' in p_line or 'Next' in p_line or 'Disp ' in p_line
                                if not test:
                                    lines_to_remove += 1
                                    if 'Sentence' in sec_lines[4] and 'Seq No' not in p_line:
                                        lines_to_remove += 1
                    elif 'Seq No' in line:
                        p_line = previous_sec_lines[-1]
                        test = 'Def' in p_line or 'Arrest' in p_line or 'Next' in p_line or 'Disp ' in p_line
                        if not test:
                            lines_to_remove += 1
                            if 'Sentence' in sec_lines[3] and 'Seq No' not in p_line:
                                lines_to_remove += 1

        for ln in sec_lines[lines_to_remove:]:
            slines.append(ln)

        previous_sec_lines = sec_lines

    # And recombine into one string.
    summary_info_combined = "\n".join(slines)

    try:
        parsed_summary_body = summary_body_grammar.parse(summary_info_combined)
    except Exception as e:
        #pytest.set_trace()
        raise e

    summary_info_visitor = CustomVisitorFactory(
        summary_body_terminals,
        summary_body_nonterminals,
        [("sentence_length", visit_sentence_length)],
    ).create_instance()

    summary_body_xml_tree = etree.fromstring(
        summary_info_visitor.visit(parsed_summary_body)
    )

    # combine the caption, header, and body info into a single xml
    # representation of the summary.
    summary._xml = etree.Element("Summary")
    summary._xml.append(pages_xml_tree.xpath("//header")[0])
    summary._xml.append(pages_xml_tree.xpath("//caption")[0])
    summary._xml.append(summary_body_xml_tree)

    return summary


class Summary:
    """
    Information from a Summary docket sheet.
    """

    text: str
    tempdir: str
    _xml: etree.Element
    parsed_pages: parsimonious.nodes.Node

    def __init__(self, pdf: Union[BinaryIO, str] = None, tempdir: str = "tmp") -> None:
        if pdf is not None:
            parse_pdf(self, pdf, tempdir)

    def get_defendant(self) -> Person:
        if self._xml is not None:
            full_name = self._xml.find("caption/defendant_name").text
            last_first = [n.strip() for n in full_name.split(",")]
            def_dob = self._xml.find("caption/def_dob").text.strip()
            try:
                def_dob = datetime.strptime(def_dob, "%m/%d/%Y").date()
            except ValueError:
                def_dob = None
            return Person(last_first[1], last_first[0], def_dob)
        return Person(None, None, None)

    def get_cases(self) -> List:
        """
        Return a list of the cases described in this Summary sheet.
        """
        cases = []
        case_elements = self._xml.xpath("//case")
        for case in case_elements:
            closed_sequences = case.xpath(".//closed_sequence")
            closed_charges = []
            for seq in closed_sequences:
                charge = Charge(
                    offense=text_or_blank(seq.find("description")),
                    statute=text_or_blank(seq.find("statute")),
                    grade=text_or_blank(seq.find("grade")),
                    disposition=text_or_blank(seq.find("sequence_disposition")),
                    sentences=[],
                )
                for sentence in seq.xpath(".//sentencing_info"):
                    charge.sentences.append(
                        Sentence(
                            sentence_date=date_or_none(sentence.find("sentence_date")),
                            sentence_type=text_or_blank(sentence.find("sentence_type")),
                            sentence_period=text_or_blank(
                                sentence.find("program_period")
                            ),
                            sentence_length=SentenceLength(
                                min_time=(
                                    text_or_blank(
                                        sentence.find("sentence_length/min_length/time")
                                    ),
                                    text_or_blank(
                                        sentence.find("sentence_length/min_length/unit")
                                    ),
                                ),
                                max_time=(
                                    text_or_blank(
                                        sentence.find("sentence_length/max_length/time")
                                    ),
                                    text_or_blank(
                                        sentence.find("sentence_length/max_length/unit")
                                    ),
                                ),
                            ),
                        )
                    )
                closed_charges.append(charge)

            open_sequences = case.xpath(".//open_sequence")
            open_charges = []
            for seq in open_sequences:
                charge = Charge(
                    offense=text_or_blank(seq.find("description")),
                    statute=text_or_blank(seq.find("statute")),
                    grade=text_or_blank(seq.find("grade")),
                    disposition=text_or_blank(seq.find("sequence_disposition")),
                    sentences=[],
                )
                for sentence in seq.xpath(".//sentencing_info"):
                    charge.sentences.append(
                        Sentence(
                            sentence_date=date_or_none(sentence.find("sentence_date")),
                            sentence_type=text_or_blank(sentence.find("sentence_type")),
                            sentence_period=text_or_blank(
                                sentence.find("program_period")
                            ),
                            sentence_length=SentenceLength(
                                min_time=(
                                    text_or_blank(
                                        sentence.find("sentence_length/min_length/time")
                                    ),
                                    text_or_blank(
                                        sentence.find("sentence_length/min_length/unit")
                                    ),
                                ),
                                max_time=(
                                    text_or_blank(
                                        sentence.find("sentence_length/max_length/time")
                                    ),
                                    text_or_blank(
                                        sentence.find("sentence_length/max_length/unit")
                                    ),
                                ),
                            ),
                        )
                    )
                open_charges.append(charge)

            cases.append(
                Case(
                    status=text_or_blank(case.getparent().getparent()),
                    county=text_or_blank(case.getparent().find("county")),
                    docket_number=text_or_blank(case.find("case_basics/docket_num")),
                    otn=text_or_blank(case.find("case_basics/otn_num")),
                    dc=text_or_blank(case.find("case_basics/dc_num")),
                    charges=closed_charges + open_charges,
                    fines_and_costs=None,  # a summary docket never has info about this.
                    arrest_date=date_or_none(
                        case.find("arrest_and_disp/arrest_date")
                    ),
                    disposition_date=date_or_none(
                        case.find("arrest_and_disp/disp_date")
                    ),
                    judge=text_or_blank(case.find("arrest_and_disp/disp_judge")),
                )
            )
        return cases
