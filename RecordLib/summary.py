from __future__ import annotations
from typing import BinaryIO, Union
import io
import parsimonious  # type: ignore
from RecordLib.grammars.summary import (
    summary_page_grammar, summary_page_terminals, summary_page_nonterminals)
from RecordLib.CustomNodeVisitorFactory import CustomVisitorFactory
import pytest
import os

def parse_pdf(summary: Summary, pdf: Union[BinaryIO,str], tempdir: str = "tmp") -> None:
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


    summary_page_visitor = CustomVisitorFactory(summary_page_terminals, summary_page_nonterminals, dict()).create_instance()
    xml_tree = summary_page_visitor.visit(summary.parsed_pages)
    pytest.set_trace()
    # Store the header information

    # combine the body sections from each page and parse the combined body

class Summary:
    """
    Information from a Summary docket sheet.
    """

    text: str
    tempdir: str

    def __init__(self, pdf:Union[BinaryIO, str] = None, tempdir: str = "tmp") -> None:
        if pdf is not None:
            parse_pdf(self, pdf, tempdir)
