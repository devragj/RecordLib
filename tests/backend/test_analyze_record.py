from RecordLib.serializers import to_serializable
import json

def test_analyze(dclient, example_crecord):
    resp = dclient.post("/record/analyze", 
        to_serializable(example_crecord), 
        format="json")
    assert resp.status_code == 200
    analysis = resp.json()
    assert all(key in ["rec", "modified_rec", "analysis"] for key in analysis.keys())