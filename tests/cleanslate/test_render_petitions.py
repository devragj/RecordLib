import pytest
from RecordLib.analysis import Analysis
from RecordLib.serializers import to_serializable
from RecordLib.ruledefs import expunge_nonconvictions
from cleanslate.models import ExpungementPetitionTemplate, SealingPetitionTemplate
import json 
from django.core.files import File

@pytest.mark.django_db
def test_render_petitions(admin_user, admin_client, example_crecord, example_attorney):
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        exp_petition = ExpungementPetitionTemplate.objects.create(
            name="790ExpungementTemplate.docx", file=File(tp))
    with open("tests/templates/791SealingTemplate.docx", 'rb') as tp:
        sealing_petition = SealingPetitionTemplate.objects.create(
            name="790SealingTemplate.docx", file=File(tp))
    
    admin_user.userprofile.expungement_petition_template = exp_petition
    admin_user.userprofile.sealing_petition_template = sealing_petition
    admin_user.userprofile.save()

    example_crecord.cases[0].charges[0].disposition = "Not Guilty"
    ans = Analysis(example_crecord).rule(expunge_nonconvictions)
    petitions = []
    for decision in ans.decisions:
        petitions.append(*decision.value)
    for p in petitions:
        p.attorney = example_attorney
    resp = admin_client.post("/record/petitions/", 
        json.dumps(
            {"petitions": petitions}, 
            default=to_serializable
        ),
        content_type="application/json")
    assert resp.status_code == 200
