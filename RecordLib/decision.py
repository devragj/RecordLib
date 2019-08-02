from __future__ import annotations
from typing import Union, List

class Decision:
    """
    Experimental class for keeping the value of a decision and the reason for it together in a single object.

    A single decision could be composed out of a bunch of smaller decisions, so that a decision can be, on one hand, made up of a bunch of other decisions, and then on the other, fully explained, including explanations for sub-decisions.

    Args:
        name: A friendy name for the decision, like "Should we go to the zoo?"
        value: The content decision. Might be True, or "Yes, go to the zoo", or anything else.
        reasoning: Either a string or a set of sub-decisions that explain the value.
    """

    def __init__(self, name: str, value: any="", reasoning: Union[str, List[Decision]]=""):
        self.name = name
        self.value = value
        self.reasoning = reasoning

    def __bool__(self):
        """
        The boolean value of a Decision should be whatever the boolean of the `value` that the decision contains.
        """
        return bool(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return self.value == other

    def as_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "reasoning": self.reasoning
        }
