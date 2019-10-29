from django.test import TestCase
from cleanslate.models import PetitionTemplate
from RecordLib.petitions import Expungement
import pytest
import io

# django unittest test, for testing the database and relying on django's built in db setup/teardowns.
class PetitionTemplateTestCase(TestCase):
    def setUp(self):
        with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
            PetitionTemplate.objects.create(name="Expungement Petition Template", data=tp.read(), doctype="docx")

    def test_petition_template_type(self):
        """  A petition template has a doctype"""
        expungement_template = PetitionTemplate.objects.get(name="Expungement Petition Template")
        self.assertEqual(expungement_template.doctype, "docx")


@pytest.mark.django_db
def test_petition_bytes():
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        PetitionTemplate.objects.create(
            name="Expungement Petition Template", data=tp.read(), doctype="docx")
    pet = PetitionTemplate.objects.get(name="Expungement Petition Template").data_as_bytesio()

# a pytest test, so i can use the fixtures
@pytest.mark.django_db
def test_render_petition(example_expungement):
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        pet = PetitionTemplate.objects.create(
            name="Expungement Petition Template", data=tp.read(), doctype="docx")
        example_expungement.set_template(pet.data_as_bytesio())
    try:
        example_expungement.render()
    except Exception as e:
        pytest.fail(str(e))
        

