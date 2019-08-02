from __future__ import annotations
from typing import BinaryIO, Union, List, Dict, Tuple, Optional, Callable
import io
import parsimonious  # type: ignore
from parsimonious.nodes import Node  # type: ignore
from RecordLib.grammars.summary import (
    summary_page_terminals,
    summary_page_nonterminals,
    summary_body_terminals,
    cp_summary_page_grammar,
    cp_summary_body_grammar,
    cp_summary_body_nonterminals,
    md_summary_page_grammar,
    md_summary_body_grammar,
    md_summary_body_nonterminals,
)
from RecordLib.CustomNodeVisitorFactory import CustomVisitorFactory
import pytest
import os
from lxml import etree
from collections import namedtuple
from datetime import datetime
import re
import logging

class Summary:
    """
    Information from a Summary docket sheet.

    Args:
        parser: a callable that takes
        raw_source: Optional. The raw source for a Summary. Right now, only a pdf file,
            or path to one.
    """

    def __init__(self, parser: Callable, raw_source: any = None, tempdir: str = "tmp") -> None:
        if raw_source is not None:
            defendant, cases = parser(raw_source, tempdir)
            self._defendant = defendant
            self._cases = cases
        else:
            self._defendant = None
            self._cases = None

    def get_defendant(self) -> Person:
        return self._defendant

    def get_cases(self) -> List:
        return self._cases
