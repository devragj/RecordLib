import pytest
from rest_framework.response import Response
from ujs.models import SourceRecord

def test_search_ujs_by_name_missing_data(admin_client):
    resp = admin_client.post('/ujs/search/name/', follow=True)
    assert resp.status_code == 400
    assert resp.data['errors']['first_name'][0].code == 'required'


def test_search_ujs_by_name(admin_client, monkeypatch):

    def mockresponse(url, data, follow):
        return(
            Response({
                'searchResults': {
                    'CP': {
                        'dockets': [
                            {
                                'caption': 'Comm. v. Smith, J.', 
                                'case_status': 'Active', 
                                'dob': '1/1/2000',
                                'docket_number': 'CP-12345',
                                'docket_sheet_url': 'https://ujsportal.pacourts.us.gov/lalala',
                                'otn':'1234',
                                'summary_url': 'https://ujsportal.pacourts.us.gov/bababa',
                            },
                        ],  
                        'msg': "Success",
                    },
                    'MDJ': {
                        'dockets': [],
                        'msg': "    Search completed. No dockets found."
                    }
                }, 
            },
            200
        )
    )
        

    monkeypatch.setattr(admin_client, 'post', mockresponse)

    resp = admin_client.post(
        '/ujs/search/name/', 
        data={
            "first_name":"Jane",
            "last_name":"Smith",
        },
        follow=True)
    assert resp.status_code == 200
    assert all( [ court in resp.data['searchResults'].keys() for court in ["CP", "MDJ"]] )


@pytest.mark.django_db
def test_download_ujs_docs(admin_client):
    """
    post a couple of documents with urls to the server. Server creates objects to store the downloaded files and then 
    returns uuids of the document objects in the database.
    """
    doc_1 = {
        "docket_num": "CP-12345",
        "court": "CP",
        "url": "https://ujsportal.pacourts.us/DocketSheets/CPReport.ashx?docketNumber=CP-25-CR-1234567-2010&dnh=12345",
        "caption": "Comm. v. SillyKitty",
        "record_type": SourceRecord.RecTypes.DOCKET_PDF,
    }
    doc_2 = {
        "docket_num": "CP-54321",
        "court": "CP",
        "url": "https://ujsportal.pacourts.us/DocketSheets/CourtSummaryReport.ashx?docketNumber=CP-25-CR-1234567-2010&dnh=12345",
        "caption": "Comm. v. SillyKitty",
        "record_type": SourceRecord.RecTypes.SUMMARY_PDF,
    }
    resp = admin_client.post(
        "/ujs/download/",
        data = {
            "source_records": [doc_1, doc_2]
        }, follow=True, content_type="application/json")
    assert resp.status_code == 200
    for rec in resp.data["source_records"]:
        try:
            rec['id']
        except:
            pytest.fail("rec in response didn't have an id")
    