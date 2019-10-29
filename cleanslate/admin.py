from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from cleanslate.models import PetitionTemplate, UserProfile
from django import forms
from django.db import models

# this doesn't work. the file input widget seems to expect to encode or decode the file
# but the binaryfield wants the actual binary.
#class PetitionTemplateAdmin(admin.ModelAdmin):
#    formfield_overrides = {
#        models.BinaryField: {'widget': forms.ClearableFileInput()}
#    }
#admin.site.register(PetitionTemplate, PetitionTemplateAdmin)
admin.site.register(PetitionTemplate)

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profiles"
    fk_name= "user"

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)