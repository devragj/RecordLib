from __future__ import annotations
from typing import BinaryIO, Union, List
import io
import parsimonious  # type: ignore
from parsimonious.nodes import Node # type: ignore
from RecordLib.grammars.summary import (
    summary_page_grammar,
    summary_page_terminals,
    summary_page_nonterminals,
    summary_body_grammar,
    summary_body_terminals,
    summary_body_nonterminals,
)
from RecordLib.CustomNodeVisitorFactory import CustomVisitorFactory
from RecordLib.common import Person, Case, Charge
import pytest
import os
from lxml import etree
from collections import namedtuple

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

    # Parse each page (a header, body, and footer)
    try:
        summary.parsed_pages = summary_page_grammar.parse(summary.text)
    except Exception as e:
        raise ValueError("Grammar cannot parse summary.")

    summary_page_visitor = CustomVisitorFactory(
        summary_page_terminals, summary_page_nonterminals, dict()
    ).create_instance()

    # the summary is now a string of xml along the lines of:
    # <summary> <first_page> ... </first_page>
    # <following_page> ... </following_page> </summary>
    pages_xml_tree = etree.fromstring(summary_page_visitor.visit(summary.parsed_pages))

    # combine the body sections from each page and parse the combined body
    summary_info_sections = pages_xml_tree.findall(".//summary_info")


    summary_info_combined = "\n".join(
        sec.text for sec in summary_info_sections if "(Continued)" not in sec.text
    )

    try:
        parsed_summary_body = summary_body_grammar.parse(summary_info_combined)
    except Exception as e:
        # lines of the text.
        # slines is for debugging and having quick access to a list of the
        slines = []
        for sec in summary_info_sections:
            for ln in sec.text.split("\n"):
                slines.append(ln)
        raise e

    summary_info_visitor = CustomVisitorFactory(
        summary_body_terminals, summary_body_nonterminals, dict()
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

    def get_defendant_name(self) -> Person:
        if self._xml is not None:
            full_name = self._xml.find("caption/defendant_name").text
            last_first = [n.strip() for n in full_name.split(",")]
            return Person(last_first[1], last_first[0])
        return Person(None, None)

    def get_cases(self) -> List:
        """
        Return a list of the cases described in this Summary sheet.
        """
        cases = []
        case_elements = self._xml.xpath("//case")
        for case in case_elements:
            closed_sequences = case.xpath("//closed_sequence")
            closed_charges = []
            for seq in closed_sequences:
                closed_charges.append(Charge(
                    offense=seq.find("description").text.strip(),
                    statute=seq.find("statute").text.strip(),
                    grade=seq.find("grade").text.strip(),
                    disposition=seq.find("sequence_disposition").text.strip()
                ))

            open_sequences = case.xpath("//open_sequence")
            open_charges = []
            for seq in open_sequences:
                raise NotImplementedError

            cases.append(Case(
                status=case.getparent().getparent().text.strip(),
                county=case.getparent().find("county").text.strip(),
                docket_numbers=[case.find("case_basics/docket_num").text.strip()
],
                otn=case.find("case_basics/otn_num").text.strip(),
                dc=case.find("case_basics/dc_num").text.strip(),
                charges=closed_charges + open_charges,
                fines_and_costs=None # a summary docket never has info about this.
            ))
        return cases
