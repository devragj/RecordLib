from django.test import TestCase
from django.core.files import File
from cleanslate.models import ExpungementPetitionTemplate, SealingPetitionTemplate
from RecordLib.petitions import Expungement
import pytest
import io

# django unittest test, for testing the database and relying on django's built in db setup/teardowns.
class PetitionTemplateTestCase(TestCase):
    def setUp(self):
        with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
            ExpungementPetitionTemplate.objects.create(name="Expungement Petition Template", file=File(tp))

    def test_petition_template_type(self):
        """  A petition template has a doctype"""
        expungement_template = ExpungementPetitionTemplate.objects.get(name="Expungement Petition Template")
        self.assertEqual(expungement_template.name, "Expungement Petition Template")


# a pytest test, so i can use the fixtures
@pytest.mark.django_db
def test_render_petition(example_expungement):
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        pet = ExpungementPetitionTemplate.objects.create(
            name="Expungement Petition Template", file=File(tp))
        example_expungement.set_template(pet.file)
    try:
        example_expungement.render()
    except Exception as e:
        pytest.fail(str(e))
        

