from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import io

class PetitionTemplate(models.Model):
    """Model for storing a docx template for expungement or sealing petitions."""
    
    name = models.CharField(max_length=255)
    doctype = models.CharField(max_length=255)  # perhaps should be a reference table of supported types.
    data = models.BinaryField(editable=True)

    def data_as_bytesio(self):
        """
        DB stores `data` as bytes, but we more often want to use a BytesIO object.
        """
        return io.BytesIO(self.data)



class UserProfile(models.Model):
    """Information unrelated to authentication that is relevant to a user. """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    expungement_petition_template = models.ForeignKey(
        PetitionTemplate, 
        on_delete=models.CASCADE,
        null=True, 
        related_name="expugement_template_user_profiles")
    sealing_petition_template = models.ForeignKey(
        PetitionTemplate,
        on_delete=models.CASCADE,
        null=True,
        related_name="sealing_petition_template_user_profiles")


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)