import functools
from RecordLib.common import Charge, SentenceLength
from RecordLib.ruledefs import Decision
from datetime import date, datetime
from dataclasses import asdict

@functools.singledispatch
def to_serializable(val):
    """
    single_dispatch is for letting me define how different classes should serialize.

    There's a single default serializer (this method), and then additional methods that replace this method depending on the type sent to the method.
    """
    return str(val)

@to_serializable.register(Charge)
def ts_charge(charge):
    return asdict(charge)

@to_serializable.register(date)
@to_serializable.register(datetime)
def ts_date(a_date):
    return a_date.isoformat()


@to_serializable.register(Decision)
def td_decision(dec):
    if isinstance(dec.reasoning, list):
        return {
            "name": to_serializable(dec.name),
            "value": to_serializable(dec.value),
            "reasoning": [to_serializable(r) for r in dec.reasoning]
        }

    return {
        "name": to_serializable(dec.name),
        "value": to_serializable(dec.value),
        "reasoning": to_serializable(dec.reasoning)
    }

@to_serializable.register(SentenceLength)
def ts_sentencelength(sentence_length):
    return f"{sentence_length.min_time} days to {sentence_length.max_time} days"
