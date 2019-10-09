import functools
from RecordLib.common import Charge, Sentence, SentenceLength
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
        "decisions": to_serializable(an.decisions),
        "remaining_record": to_serializable(an.remaining_record),
        "record": to_serializable(an.record)
    }


@to_serializable.register(Sealing)
def td_sealing(s):
    return {
        "petition_type": to_serializable(s.petition_type),
        "client": to_serializable(s.client),
        "cases": to_serializable(s.cases),
        "attorney": to_serializable(s.attorney),
        "summary_expungement_language": to_serializable(s.summary_expungement_language),
        "include_crim_hist_report": to_serializable(s.include_crim_hist_report),
        "ifp_message": to_serializable(s.ifp_message),
    }

@to_serializable.register(Expungement)
def td_expungement(e):
    return {
        "petition_type": to_serializable(e.petition_type),
        "attorney": to_serializable(e.attorney),
        "expungement_type": to_serializable(e.expungement_type),
        "procedure": to_serializable(e.procedure),
        "client": to_serializable(e.client),
        "cases": to_serializable(e.cases),
        "summary_expungement_language": to_serializable(e.summary_expungement_language),
        "include_crim_hist_report": to_serializable(e.include_crim_hist_report),
        "ifp_message": to_serializable(e.ifp_message),
    }

@to_serializable.register(Attorney)
def td_attorney(atty):
    return {
        "organization": to_serializable(atty.organization),
        "name": to_serializable(atty.name),
        "organization_address": to_serializable(atty.organization_address),
        "organization_phone": to_serializable(atty.organization_phone),
        "bar_id": to_serializable(atty.bar_id) 
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

