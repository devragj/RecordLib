from RecordLib.summary.pdf import parse_pdf
from RecordLib.serializers import to_serializable
import os
import json

def test_upload_record(admin_client, example_summary):
    filename = os.listdir("tests/data/summaries")[1]
    path = os.path.join("tests/data/summaries", filename )
    with open(path, 'rb') as f: 
        resp = admin_client.post("/record/upload/", {'files': [f]})
    assert resp.status_code == 200
    records = resp.json()
    assert "source_records" in records.keys()
    assert len(records['source_records']) == 1
    assert records['source_records'][0]['record_type'] == "SUMMARY_PDF"