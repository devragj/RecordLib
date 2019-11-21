import pytest
from cleanslate.models import UserProfile
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_profile_created_on_postsave():
    usr = User.objects.create_user(
        username="Test",
        password="test"
    )
    usr.save()
    try:
        usr.userprofile
    except:
        pytest.fail( "usr doesn't seem to have a profile attached to it")
        