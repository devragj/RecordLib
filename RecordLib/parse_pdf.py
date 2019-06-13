"""
Parse a pdf to a CRecord
"""
from CRecord import CRecord
import parsimonious
from PyPDF2 import PdfFileReader


def parse_pdf(pdf: file) -> CRecord:
    dk = PdfFileReader(pdf)
    txt = "\n".join([page.extractText() for page in dk.pages])
    return CRecord()
