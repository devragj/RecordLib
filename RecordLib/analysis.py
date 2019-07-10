from __future__ import annotations
from typing import Callable
from RecordLib.crecord import CRecord
import copy
from collections import OrderedDict

class Analysis:

    def __init__(self, rec: CRecord) -> None:
        self.rec = rec
        self.modified_rec = copy.deepcopy(rec)
        self.analysis = OrderedDict()

    def rule(self, ruledef: Callable) -> Analysis:
        modified_rec, analysis = ruledef(self.modified_rec)
        self.modified_rec = modified_rec
        self.analysis.update(analysis)
        return self
