import pytest



def test_anonymous_cannot_get_userprofileview(dclient):
    resp = dclient.get('/record/profile/', follow=True)
    assert resp.status_code == 403 

def test_loggedin_get_userprofileview(admin_client):
    resp = admin_client.get('/record/profile/', follow=True)
    assert resp.status_code == 200
    userdata = resp.data
    assert 'user' in userdata.keys()
    assert 'profile' in userdata.keys()
