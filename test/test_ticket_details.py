#!/usr/bin/env python3.9
"""
Test the `ticket_details.py` file under main/upstream.
"""

import pytest
import json

from main.upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE
from main.upstream.ticket_details import TicketDetails


@pytest.fixture()
def td_instance():
    """
    Initialize and yield an instance of the TicketDetails class.
    """
    td: TicketDetails = TicketDetails(api_url_root=API_URL_ROOT, auth_tuple=AUTH_TUPLE)
    yield td


@pytest.fixture()
def resp():
    """
    Provide test responses from the Zendesk API.
    """
    class Responses:
        ticket_success: dict = json.loads("""
        {"ticket":{"url":"https://zccsammdu.zendesk.com/api/v2/tickets/2.json","id":2,"external_id":null,"via":{"channel":"api","source":{"from":{},"to":{},"rel":null}},"created_at":"2021-11-27T07:00:17Z","updated_at":"2021-11-28T03:59:12Z","type":null,"subject":"velit eiusmod reprehenderit officia cupidatat","raw_subject":"velit eiusmod reprehenderit officia cupidatat","description":"Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\\n\\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.","priority":null,"status":"pending","recipient":null,"requester_id":1910383993885,"submitter_id":1910383993885,"assignee_id":1910383993885,"organization_id":1500634551141,"group_id":4411226980499,"collaborator_ids":[],"follower_ids":[],"email_cc_ids":[],"forum_topic_id":null,"problem_id":null,"has_incidents":false,"is_public":true,"due_at":null,"tags":["est","incididunt","nisi"],"custom_fields":[],"satisfaction_rating":null,"sharing_agreement_ids":[],"fields":[],"followup_ids":[],"ticket_form_id":1500003309421,"brand_id":1500002344441,"allow_channelback":false,"allow_attachments":true}}
        """)

        user_success: dict = json.loads("""
        {"user":{"id":1910383993885,"url":"https://zccsammdu.zendesk.com/api/v2/users/1910383993885.json","name":"Samm Du","email":"contact@sammdu.com","created_at":"2021-11-24T20:56:30Z","updated_at":"2021-11-30T07:45:33Z","time_zone":"Eastern Time (US & Canada)","iana_time_zone":"America/New_York","phone":null,"shared_phone_number":null,"photo":{"url":"https://zccsammdu.zendesk.com/api/v2/attachments/1501105037121.json","id":1501105037121,"file_name":"pixel-art-bc_0.5-in_1500ppi.png","content_url":"https://zccsammdu.zendesk.com/system/photos/1501105037121/pixel-art-bc_0.5-in_1500ppi.png","mapped_content_url":"https://zendesk.sammdu.com/system/photos/1501105037121/pixel-art-bc_0.5-in_1500ppi.png","content_type":"image/png","size":1117,"width":80,"height":80,"inline":false,"deleted":false,"thumbnails":[{"url":"https://zccsammdu.zendesk.com/api/v2/attachments/1501105037141.json","id":1501105037141,"file_name":"pixel-art-bc_0.5-in_1500ppi_thumb.png","content_url":"https://zccsammdu.zendesk.com/system/photos/1501105037121/pixel-art-bc_0.5-in_1500ppi_thumb.png","mapped_content_url":"https://zendesk.sammdu.com/system/photos/1501105037121/pixel-art-bc_0.5-in_1500ppi_thumb.png","content_type":"image/png","size":504,"width":32,"height":32,"inline":false,"deleted":false}]},"locale_id":1,"locale":"en-US","organization_id":1500634551141,"role":"admin","verified":true,"external_id":null,"tags":[],"alias":null,"active":true,"shared":false,"shared_agent":false,"last_login_at":"2021-11-30T07:45:33Z","two_factor_auth_enabled":null,"signature":null,"details":null,"notes":null,"role_type":null,"custom_role_id":null,"moderator":true,"ticket_restriction":null,"only_private_comments":false,"restricted_agent":false,"suspended":false,"default_group_id":4411226980499,"report_csv":true,"user_fields":{}}}
        """)

        common_404: dict = {
            "error": "RecordNotFound",
            "description": "Not found"
        }

        user_400: dict = {
            "error": {
                "title": "Invalid attribute",
                "message": "You passed an invalid value for the id attribute. " +
                           "Invalid parameter: id must be an integer from api/v2/users/show"
            }
        }

    yield Responses


def test_init(td_instance):
    """
    Test the __init__() method, make sure it records the correct information.
    """
    assert td_instance.api_url_root == API_URL_ROOT
    assert td_instance.auth_tuple == AUTH_TUPLE


def test_request_ticket_success(td_instance, resp, requests_mock):
    """
    Test the _request_ticket() method, make sure it returns the correct data upon a
    successful call.
    """
    MOCK_TICKET_URL: str = "https://zccsammdu.zendesk.com/api/v2/tickets/2.json"

    requests_mock.get(MOCK_TICKET_URL, json=resp.ticket_success)
    response: dict = td_instance._request_ticket(MOCK_TICKET_URL)

    assert response == resp.ticket_success['ticket']


def test_request_ticket_failure_404(td_instance, resp, requests_mock):
    """
    Test the _request_ticket() method, make sure it returns {} upon a 404 HTTP error.
    """
    MOCK_TICKET_URL: str = "https://zccsammdu.zendesk.com/api/v2/tickets/xyz.json"

    requests_mock.get(MOCK_TICKET_URL, json=resp.common_404, status_code=404)
    response: dict = td_instance._request_ticket(MOCK_TICKET_URL)

    assert response == {}


def test_request_user_success(td_instance, resp, requests_mock):
    """
    Test the _request_user() method, make sure it returns the correct data upon a
    successful call.
    """
    MOCK_USER_ID: str = "1910383993885"
    MOCK_USER_URL: str = f"https://zccsammdu.zendesk.com/api/v2/users/{MOCK_USER_ID}.json"

    requests_mock.get(MOCK_USER_URL, json=resp.user_success)
    response: dict = td_instance._request_user(MOCK_USER_ID)

    assert response == resp.user_success['user']


def test_request_user_failure_404(td_instance, resp, requests_mock):
    """
    Test the _request_user() method, make sure it returns {} upon a 404 HTTP error.
    """
    MOCK_USER_ID: str = "1910383993000"
    MOCK_USER_URL: str = f"https://zccsammdu.zendesk.com/api/v2/users/{MOCK_USER_ID}.json"

    requests_mock.get(MOCK_USER_URL, json=resp.common_404, status_code=404)
    response: dict = td_instance._request_user(MOCK_USER_ID)

    assert response == {}


def test_request_user_failure_400(td_instance, resp, requests_mock):
    """
    Test the _request_user() method, make sure it returns {} upon a 400 HTTP error.
    """
    MOCK_USER_ID: str = "1910383993xyz"
    MOCK_USER_URL: str = f"https://zccsammdu.zendesk.com/api/v2/users/{MOCK_USER_ID}.json"

    requests_mock.get(MOCK_USER_URL, json=resp.user_400, status_code=400)
    response: dict = td_instance._request_user(MOCK_USER_ID)

    assert response == {}


def test_get_ticket_success(td_instance, resp, requests_mock):
    """
    Test the get_ticket() method, make sure it returns the correct data upon a
    successful call.
    """
    MOCK_TICKET_URL: str = "https://zccsammdu.zendesk.com/api/v2/tickets/2.json"
    MOCK_USER_URL: str = "https://zccsammdu.zendesk.com/api/v2/users/1910383993885.json"

    requests_mock.get(MOCK_TICKET_URL, json=resp.ticket_success)
    requests_mock.get(MOCK_USER_URL, json=resp.user_success)
    response: dict = td_instance.get_ticket(MOCK_TICKET_URL)

    correct_response: dict = resp.ticket_success['ticket']
    correct_response['requester'] = resp.user_success['user']
    correct_response['assignee'] = resp.user_success['user']

    assert response == correct_response


def test_get_ticket_failure_noticket(td_instance, resp, requests_mock):
    """
    Test the get_ticket() method, make sure it returns {} when the ticket details cannot
    be fetched.
    """
    MOCK_TICKET_URL: str = "https://zccsammdu.zendesk.com/api/v2/tickets/2.json"
    MOCK_USER_URL: str = "https://zccsammdu.zendesk.com/api/v2/users/1910383993885.json"

    requests_mock.get(MOCK_TICKET_URL, json=resp.common_404)
    requests_mock.get(MOCK_USER_URL, json=resp.user_success)
    response: dict = td_instance.get_ticket(MOCK_TICKET_URL)

    assert response == {}


def test_get_ticket_failure_nouser(td_instance, resp, requests_mock):
    """
    Test the get_ticket() method, make sure it returns {} when the relevant user details
    cannot be fetched.
    """
    MOCK_TICKET_URL: str = "https://zccsammdu.zendesk.com/api/v2/tickets/2.json"
    MOCK_USER_URL: str = "https://zccsammdu.zendesk.com/api/v2/users/1910383993885.json"

    requests_mock.get(MOCK_TICKET_URL, json=resp.ticket_success)
    requests_mock.get(MOCK_USER_URL, json=resp.common_404)
    response: dict = td_instance.get_ticket(MOCK_TICKET_URL)

    assert response == {}
