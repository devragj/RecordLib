from __future__ import annotations
from typing import Callable
from RecordLib.crecord import CRecord
import copy
from collections import OrderedDict

class Analysis:

    def __init__(self, rec: CRecord) -> None:
        self.rec = rec
        self.modified_rec = copy.deepcopy(rec)
        self.decisions = []

    def rule(self, ruledef: Callable) -> Analysis:
        """
        Apply the rule `ruledef` to this analysis. 

        Args:
            ruledef (callable): ruledef is a callable. It takes a `crecord` as the only parameter. 
                It returns a tuple like (CRecord, Decision). The CRecord is whatever cases and charges remain
                on the input CRecord after applying `ruledef`. The Decision is an analysis of the record's
                eligibility for sealing or expungement. The Decision has a plain-langage `name`. It has a `value`
                that is a list of `Petiion` objects. And it has a `reasoning` that is a list of `Decisions` which
                explain how the rule decided what Petitions should be created.

        Returns:
            This Analyis, after applying the ruledef and updating the analysis with the results of the ruledef.
        """
        modified_rec, decision = ruledef(self.modified_rec)
        self.modified_rec = modified_rec
        self.decisions.append(decision)
        return self
