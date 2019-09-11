"""
Classes representing expungment or sealing petitions. 

TODO These are really just stubs for now while I'm working on what the Analysis and ruledef function signatures look like.
"""
from RecordLib.case import Case
from RecordLib.common import Person
from typing import Optional, List

class Petition:

    def __init__(self, person: Optional[Person] = None, cases: Optional[List[Case]] = None) -> None:
        self.cases = cases or []
        self.person = person

    def add_case(case: Case) -> None:
        self.cases.append(case)

    def __repr__(self):
        return (f"Petition(Person: {self.person}, Cases: {[c for c in self.cases]})")

class Expungement(Petition):
    # class-level constants for the type of the expungment.
    FULL_EXPUNGEMENT = "Full Expungement"
    PARTIAL_EXPUNGEMENT = "Partial Expungement"
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ""        

    def __repr__(self):
        return (f"Petition({self.type}, Person: {self.person}, Cases: {[c for c in self.cases]})")



class Sealing(Petition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)