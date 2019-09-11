import functools
from RecordLib.common import Charge, Person, Sentence, SentenceLength
from RecordLib.case import Case
from RecordLib.analysis import Analysis
from RecordLib.petitions import Expungement, Sealing
from RecordLib.decision import Decision
from RecordLib.crecord import CRecord
from datetime import date, datetime, timedelta


@functools.singledispatch
def to_serializable(val):
    """
    single_dispatch is for letting me define how different classes should serialize.

    There's a single default serializer (this method), and then additional methods that replace this method
    depending on the type sent to the method.
    """
    return str(val)

@to_serializable.register(type(None))
def td_none(n):
    return ""

@to_serializable.register(list)
def ts_list(a_list):
    return [to_serializable(i) for i in a_list]

@to_serializable.register(list)
def ts_list(l):
    if len(l) == 0:
        return []
    return [to_serializable(el) for el in l]

@to_serializable.register(Case)
@to_serializable.register(Charge)
@to_serializable.register(Person)
@to_serializable.register(Sentence)
def ts_object(an_object):
    return {k:to_serializable(v) for k, v in an_object.__dict__.items() if v is not None}


@to_serializable.register(date)
@to_serializable.register(datetime)
def ts_date(a_date):
    return a_date.isoformat()


@to_serializable.register(timedelta)
def ts_date(a_delta):
    return str(a_delta)


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

@to_serializable.register(Analysis)
def td_analysis(an):
    return {
        "analysis": an.decisions,
        "remaining_record": an.modified_rec,
        "original_record": an.rec
    }


@to_serializable.register(Sealing)
def td_sealing(s):
    return {
        "petition": "Sealing",
        "person": s.person,
        "cases": s.cases
    }

@to_serializable.register(Expungement)
def td_sealing(e):
    return {
        "petition": "Expungement",
        "type": e.type,
        "person": e.person,
        "cases": e.cases
    }


@to_serializable.register(CRecord)
def td_crecord(crec):
    return {
        "person": to_serializable(crec.person),
        "cases": [to_serializable(c) for c in crec.cases]
    }

    
@to_serializable.register(SentenceLength)
def ts_sentencelength(sentence_length):
     return {
         "min_time": sentence_length.min_time.days,
         "min_unit": "days",
         "max_time": sentence_length.max_time.days,
         "max_unit": "days"
     }

