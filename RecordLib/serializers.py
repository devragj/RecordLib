import functools
from RecordLib.common import Charge, Sentence, SentenceLength, Address
from RecordLib.person import Person
from RecordLib.case import Case
from RecordLib.analysis import Analysis
from RecordLib.petitions import Expungement, Sealing
from RecordLib.decision import Decision
from RecordLib.crecord import CRecord
from RecordLib.attorney import Attorney
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
@to_serializable.register(Decision)
@to_serializable.register(Analysis)
@to_serializable.register(Sealing)
@to_serializable.register(Expungement)
@to_serializable.register(Attorney)
@to_serializable.register(CRecord)
@to_serializable.register(Address)
def ts_object(an_object):
    return {k:to_serializable(v) for k, v in an_object.__dict__.items() if v is not None}
    # return {k: to_serializable(v) for k, v in an_object.__dict__.items()}


@to_serializable.register(date)
@to_serializable.register(datetime)
def ts_date(a_date):
    return a_date.isoformat()


@to_serializable.register(timedelta)
def ts_date(a_delta):
    return str(a_delta)

    
@to_serializable.register(SentenceLength)
def ts_sentencelength(sentence_length):
     return {
         "min_time": sentence_length.min_time.days,
         "min_unit": "days",
         "max_time": sentence_length.max_time.days,
         "max_unit": "days"
     }

