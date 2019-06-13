from __future__ import annotations
from typing import BinaryIO
import parsimonious # type: ignore
from PyPDF2 import PdfFileReader
from RecordLib.grammars.summary import summary_grammar
import pytest

def parse_pdf(summary: Summary, pdf: BinaryIO) -> None:
    """
    parse a pdf and store different information about the parsing in
    summary
    """
    try:
        reader = PdfFileReader(pdf)
        summary.lines = [
            page.extractText() for page in reader.pages
        ]
        summary.text = "\n".join(summary.lines)
    except:
        raise ValueError("Cannot extract summary text..")

    try:
        summary.parsed = summary_grammar.parse(summary.text)
    except Exception as e:
        pytest.set_trace()
        raise ValueError("Grammar cannot parse summary.")

class Summary:
    """
    Information from a Summary docket sheet.
    """
    text: str

    def __init__(self, pdf=None):
        if pdf is not None:
            parse_pdf(self, pdf)
