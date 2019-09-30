
from rest_framework import serializers as S
from RecordLib.crecord import (
    CRecord
)
from RecordLib.case import Case
from RecordLib.person import Person
from RecordLib.common import (Charge, Sentence, SentenceLength)

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
    grade = S.CharField(required=False)
    statute = S.CharField(required=False)
    disposition = S.CharField(required=False)
    disposition_date = S.DateField(required=False)
    sentences = SentenceSerializer(many=True)


class CaseSerializer(S.Serializer):
    status = S.CharField(required=False)
    county = S.CharField(required=False)
    docket_number = S.CharField()
    otn = S.CharField(required=False)
    dc = S.CharField(required=False)
    charges = ChargeSerializer(many=True)
    total_fines = S.IntegerField()
    fines_paid = S.IntegerField()
    complaint_date = S.DateField(required=False)
    arrest_date = S.DateField(required=False)
    disposition_date = S.DateField(required=False)
    judge = S.CharField(required=False)
    judge_address = S.CharField(required=False)
    affiant = S.CharField(required=False)
    arresting_agency = S.CharField(required=False)
    arresting_agency_address = S.CharField(required=False)

class AttorneySerializer(S.Serializer):
    organization = S.CharField(required=False)
    name = S.CharField(required=False)
    organization_address = S.CharField(required=False)
    organization_phone = S.CharField(required=False)
    bar_id = S.CharField(required=False)


class PersonSerializer(S.Serializer):
    first_name = S.CharField(max_length=200)
    last_name = S.CharField(max_length=200)
    date_of_birth = S.DateField()
    date_of_death = S.DateField(required=False)
    aliases = S.ListField(child=S.CharField(), required=False) # CharField() doesn't seem to take many=True. 
    ssn = S.CharField(max_length=15)
    address = S.CharField(required=False)

class CRecordSerializer(S.Serializer):
    person = PersonSerializer()
    cases = CaseSerializer(many=True)

class PetitionSerializer(S.Serializer):
    attorney = AttorneySerializer()
    client = PersonSerializer()
    cases = CaseSerializer(many=True)
    expungement_type = S.CharField(required=False)
    petition_type = S.CharField(required=True)
    summary_expungement_language = S.CharField(required=False, allow_blank=True)
    service_agencies = S.ListField(child=S.CharField(), required=False)
    include_crim_hist_report = S.CharField(required=False, allow_blank=True)
    ifp_message = S.CharField(required=False, allow_blank=True)

class DocumentRenderSerializer(S.Serializer):
    petitions = PetitionSerializer(many=True)

