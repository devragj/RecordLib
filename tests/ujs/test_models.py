from ujs.models import (
    SourceRecord
)
import pytest

pytest.mark.django_db
def test_create_source_record(admin_user):
    rec_model = SourceRecord(
        caption="Comm. v. Smith",
        docket_num="CP-1234", 
        court=SourceRecord.Courts.CP,
        url="https://ujsportal.gov", 
        record_type=SourceRecord.RecTypes.SUMMARY_PDF,
        owner=admin_user)
    rec_model.save()
    new_id = rec_model.id
    saved_model = SourceRecord.objects.get(id=new_id)
    saved_model.caption == "Comm v. Smith"
    saved_model.fetch_status == SourceRecord.Statuses.NOT_FETCHED
    saved_model.file is None