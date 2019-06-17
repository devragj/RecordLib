"""
Parse a pdf to a CRecord
"""
import parsimonious  # type: ignore
from PyPDF2 import PdfFileReader  # type: ignore
from RecordLib.crecord import CRecord

from typing import BinaryIO


def parse_pdf(pdf: BinaryIO) -> CRecord:
    dk = PdfFileReader(pdf)
    txt = "\n".join([page.extractText() for page in dk.pages])
    return CRecord()
