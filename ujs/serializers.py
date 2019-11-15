from rest_framework import serializers as S
from .models import SourceRecord

class NameSearchSerializer(S.Serializer):
    """ 
    Validate json that is asking for a search of a particular name on ujs.
    """
    first_name = S.CharField(required=True)
    last_name = S.CharField(required=True)
    dob = S.DateField(required=False, default=None)



class SourceRecordSerializer(S.ModelSerializer):
    """ 
    Validate json that represents a criminal record source document, e.g., a summary pdf or docket pdf.
    """
    class Meta:
        model = SourceRecord
        exclude = [
            "owner", # only the database knows who owns what files
            "file"]  # the file itself isn't sent back and forth as a SourceRecord. The SourceRecord is a pointer to a file in the server.
    id = S.UUIDField(format='hex_verbose', required=False)



class DownloadDocsSerializer(S.Serializer):
    """
    Validate json of a POST that contains source records (a collection of objects validated by SourceRecordSerializer)
    """
    source_records = SourceRecordSerializer(many=True)

    def create(self, validated_data):
        owner = validated_data.pop("owner")
        return [SourceRecord.objects.create(**rec, owner=owner) for rec in validated_data["source_records"]]