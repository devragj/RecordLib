
from rest_framework import serializers as S
from cleanslate.models import UserProfile
from django.contrib.auth.models import User
from RecordLib.crecord import (
    CRecord
)
from RecordLib.case import Case
from RecordLib.person import Person
from RecordLib.common import (Charge, Sentence, SentenceLength)
from ujs.serializers import SourceRecordSerializer

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
    min_time = S.DurationField(required=False) #S.IntegerField(required=False)
    min_unit = S.CharField(required=False)
    max_time = S.DurationField(required=False) #S.IntegerField(required=False)
    max_unit = S.CharField(required=False) 

class SentenceSerializer(S.Serializer):
    sentence_date = S.DateField()
    sentence_type = S.CharField()
    sentence_period = S.CharField(required=False, allow_blank=True)
    sentence_length = SentenceLengthSerializer()


class ChargeSerializer(S.Serializer):
    offense = S.CharField()
    grade = S.CharField(required=False, allow_blank=True, allow_null=True, default="")
    statute = S.CharField(required=False, allow_blank=True, allow_null=True, default="")
    disposition = S.CharField(required=False, allow_blank=True, allow_null=True, default="")
    disposition_date = S.DateField(required=False, allow_null=True)
    sentences = SentenceSerializer(many=True, allow_empty=True)


class CaseSerializer(S.Serializer):
    status = S.CharField(required=False, allow_blank=True)
    county = S.CharField(required=False, allow_blank=True)
    docket_number = S.CharField(required=True)
    otn = S.CharField(required=False, allow_blank=True)
    dc = S.CharField(required=False, allow_blank=True)
    charges = ChargeSerializer(many=True, allow_null=True)
    total_fines = S.IntegerField(required=False, default=0, allow_null=True)
    fines_paid = S.IntegerField(required=False, default=0, allow_null=True)
    complaint_date = S.DateField(required=False, allow_null=True)
    arrest_date = S.DateField(required=False, allow_null=True)
    disposition_date = S.DateField(required=False, allow_null=True)
    judge = S.CharField(required=False, allow_blank=True, allow_null=True)
    judge_address = S.CharField(required=False, allow_blank=True, default="", allow_null=True)
    affiant = S.CharField(required=False, allow_blank=True, allow_null=True)
    arresting_agency = S.CharField(required=False, allow_blank=True, default="", allow_null=True)
    arresting_agency_address = S.CharField(required=False, allow_blank=True, default="", allow_null=True)

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
    first_name = S.CharField(max_length=200, allow_blank=True)
    last_name = S.CharField(max_length=200, allow_blank=True)
    date_of_birth = S.DateField(required=False, allow_null=True)
    date_of_death = S.DateField(required=False, allow_null=True)
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


class IntegrateSourcesSerializer(S.Serializer):
    crecord = CRecordSerializer()
    source_records = SourceRecordSerializer(many=True, allow_empty=True)
