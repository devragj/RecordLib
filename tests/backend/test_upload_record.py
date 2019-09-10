from RecordLib.summary.pdf import parse_pdf
from RecordLib.serializers import to_serializable
import os
import json

def test_upload_record(dclient, example_summary):
    path = os.path.join("tests/data/summaries", os.listdir("tests/data/summaries")[1])
    with open(path, 'rb') as f: 
        resp = dclient.post("/upload/", {'file': f})
    assert resp.status_code == 200
    record = json.loads(resp.json())
    assert "defendant" in record.keys()
    assert "cases" in record.keys() 