import pytest
from RecordLib.analysis import Analysis
from RecordLib.serializers import to_serializable
from RecordLib.ruledefs import expunge_nonconvictions

def test_render_petitions(dclient, example_crecord, example_attorney):
    example_crecord.cases[0].charges[0].disposition = "Not Guilty"
    ans = Analysis(example_crecord).rule(expunge_nonconvictions)
    petitions = []
    for decision in ans.decisions:
        petitions.append(*decision.value)
    for p in petitions:
        p.attorney = example_attorney
    resp = dclient.post("/record/petitions/", {"petitions": to_serializable(petitions)}, 
        format="json")
    assert resp.status_code == 200
    assert "Expunge" in resp.json()["download"]