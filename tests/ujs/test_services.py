import pytest
from ujs.models import SourceRecord
from ujs.services import download
from datetime import datetime
import logging
import time
import requests

class FakeResponse:

    def __init__(self):
        self.content = b'some bytes content'
        self.status_code = 200


def test_download_source_records(admin_user, monkeypatch):

    def slow_get(*args, **kwargs):
        time.sleep(3)
        return FakeResponse()

    monkeypatch.setattr(requests, 'get', slow_get)

    rec = SourceRecord.objects.create(
        caption="Test v Test",
        docket_num="CP-1234",
        court=SourceRecord.Courts.CP,
        url="https://some.slow.url",
        record_type=SourceRecord.RecTypes.SUMMARY_PDF,
        owner=admin_user,
    )
    rec.save()
    assert rec.file.name is None
    before = datetime.now()
    recs = [
        rec, rec, rec
    ]
    download.source_records(recs)
    after = datetime.now()
    time_spent = after - before
    assert rec.file.name is not None
    # use pytest --log-cli-level info to see this.
    logging.info(f"downloading {len(recs)} document took {time_spent.total_seconds()} seconds.")
