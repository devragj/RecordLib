
from rest_framework import serializers as S
from cleanslate.models import UserProfile
from django.contrib.auth.models import User
from RecordLib.crecord import (
    CRecord
)
from RecordLib.case import Case
from RecordLib.person import Person
from RecordLib.common import (Charge, Sentence, SentenceLength)

class UserSerializer(S.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileSerializer(S.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id']

"""
These serializer classes are only for serializing and deserializing json/dict representations of these 
classes. Use each class's `from_dict` static method to actually get the object. 


Serializers also act like data validators for data in requests to the api.
"""

class FileUploadSerializer(S.Serializer):
    files = S.ListField(child=S.FileField(), allow_empty=True)

class SentenceLengthSerializer(S.Serializer):
    min_time = S.IntegerField(required=False)
    min_unit = S.CharField(required=False)
    max_time = S.IntegerField(required=False)
    max_unit = S.CharField(required=False) 

class SentenceSerializer(S.Serializer):
    sentence_date = S.DateField()
    sentence_type = S.CharField()
    sentence_period = S.CharField(required=False, allow_blank=True)
    sentence_length = SentenceLengthSerializer()


class ChargeSerializer(S.Serializer):
    offense = S.CharField()
    grade = S.CharField(required=False, allow_blank=True)
    statute = S.CharField(required=False, allow_blank=True)
    disposition = S.CharField(required=False, allow_blank=True)
    disposition_date = S.DateField(required=False)
    sentences = SentenceSerializer(many=True)


class CaseSerializer(S.Serializer):
    status = S.CharField(required=False, allow_blank=True)
    county = S.CharField(required=False, allow_blank=True)
    docket_number = S.CharField(required=True)
    otn = S.CharField(required=False, allow_blank=True)
    dc = S.CharField(required=False, allow_blank=True)
    charges = ChargeSerializer(many=True)
    total_fines = S.IntegerField(required=False)
    fines_paid = S.IntegerField(required=False)
    complaint_date = S.DateField(required=False)
    arrest_date = S.DateField(required=False)
    disposition_date = S.DateField(required=False)
    judge = S.CharField(required=False, allow_blank=True)
    judge_address = S.CharField(required=False, allow_blank=True)
    affiant = S.CharField(required=False, allow_blank=True)
    arresting_agency = S.CharField(required=False, allow_blank=True)
    arresting_agency_address = S.CharField(required=False, allow_blank=True)

class AddressSerializer(S.Serializer):
    line_one = S.CharField()
    city_state_zip = S.CharField()

class AttorneySerializer(S.Serializer):
    organization = S.CharField(required=False)
    full_name = S.CharField(required=False)
    organization_address = AddressSerializer(required=False)
    organization_phone = S.CharField(required=False)
    bar_id = S.CharField(required=False)

class PersonSerializer(S.Serializer):
    first_name = S.CharField(max_length=200)
    last_name = S.CharField(max_length=200)
    date_of_birth = S.DateField()
    date_of_death = S.DateField(required=False)
    aliases = S.ListField(child=S.CharField(), required=False) # CharField() doesn't seem to take many=True. 
    ssn = S.CharField(max_length=15, required=False, allow_blank=True)
    address = AddressSerializer(required=False)

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

