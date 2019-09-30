from RecordLib.serializers import to_serializable
from RecordLib.petitions import Petition
import json

def test_analyze(dclient, example_crecord):
    resp = dclient.post("/record/analyze", 
        to_serializable(example_crecord), 
        format="json")
    assert resp.status_code == 200
    analysis = resp.json()
    assert all(key in ["record", "remaining_record", "decisions"] for key in analysis.keys())
    decisions = analysis["decisions"]
    petitions = [p for d in decisions for p in d["value"]]
    assert all("petition_type" in p.keys() for p in petitions)