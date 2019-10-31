from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import io

class DocumentTemplate(models.Model):
    """Abstact model for storing a template for expungement or sealing petitions."""
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="templates/")
    default = models.BooleanField(null=True)


    class Meta:
        abstract = True
    #def data_as_bytesio(self):
    #    """
    #    DB stores `data` as bytes, but we more often want to use a BytesIO object.
    #    """
    #    return io.BytesIO(self.data)

class ExpungementPetitionTemplate(DocumentTemplate):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['default'], condition=models.Q(default=True), name='unique_default_expungement_petition')
        ]
    pass

class SealingPetitionTemplate(DocumentTemplate):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['default'], condition=models.Q(default=True), name='unique_default_sealing_petition')
        ]
    pass


class UserProfile(models.Model):
    """Information unrelated to authentication that is relevant to a user. """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    expungement_petition_template = models.ForeignKey(
        ExpungementPetitionTemplate, 
        on_delete=models.CASCADE,
        null=True, 
        related_name="expugement_template_user_profiles")
    sealing_petition_template = models.ForeignKey(
        SealingPetitionTemplate,
        on_delete=models.CASCADE,
        null=True,
        related_name="sealing_petition_template_user_profiles")


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)


def set_default_templates(sender, **kwargs):
    """ 
    Set the default templates to a new user's templates, 
    If the user hasn't picked any templates, and if there are 
    default templates in the database.
    """
    profile = kwargs["instance"]
    if kwargs["created"]:
        if (profile.expungement_petition_template is None and 
                ExpungementPetitionTemplate.objects.filter(default__exact=True).count() == 1):
            profile.expungement_petition_template = (ExpungementPetitionTemplate
                .objects
                .filter(default__exact=True)
                .all()[0])
        if (profile.sealing_petition_template is None and 
                SealingPetitionTemplate.objects.filter(default__exact=True).count() == 1):
            profile.sealing_petition_template = (SealingPetitionTemplate
                .objects
                .filter(default__exact=True)
                .all()[0])

        profile.save()


post_save.connect(set_default_templates, sender=UserProfile)