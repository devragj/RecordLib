
from rest_framework import serializers as S
from RecordLib.crecord import (
    CRecord
)
from RecordLib.case import Case
from RecordLib.common import (Person, Charge, Sentence, SentenceLength)

"""
These serializer classes are only for serializing and deserializing json/dict representations of these 
classes. Use each class's `from_dict` static method to actually get the object. 
"""

class SentenceLengthSerializer(S.Serializer):
    min_time = S.IntegerField(required=False)
    min_unit = S.CharField(required=False)
    max_time = S.IntegerField(required=False)
    max_unit = S.CharField(required=False) 

class SentenceSerializer(S.Serializer):
    sentence_date = S.DateField()
    sentence_type = S.CharField()
    sentence_period = S.CharField()
    sentence_length = SentenceLengthSerializer()


class ChargeSerializer(S.Serializer):
    offense = S.CharField()
    grade = S.CharField()
    statute = S.CharField()
    disposition = S.CharField()
    sentences = SentenceSerializer(many=True)


class CaseSerializer(S.Serializer):
    status = S.CharField(required=False)
    county = S.CharField(required=False)
    docket_number = S.CharField()
    otn = S.CharField()
    dc = S.CharField()
    charges = ChargeSerializer(many=True)
    fines_and_costs = S.IntegerField()
    arrest_date = S.DateField(required=False)
    disposition_date = S.DateField(required=False)
    judge = S.CharField()




class PersonSerializer(S.Serializer):
    first_name = S.CharField(max_length=200)
    last_name = S.CharField(max_length=200)
    date_of_birth = S.DateField()
    date_of_death = S.DateField(required=False)



class CRecordSerializer(S.Serializer):
    person = PersonSerializer()
    cases = CaseSerializer(many=True)

