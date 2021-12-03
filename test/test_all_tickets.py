#!/usr/bin/env python3.9
"""
Test the `all_tickets.py` file under main/upstream.
"""

import pytest
import json

from main.upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE
from main.upstream.all_tickets import AllTickets


@pytest.fixture()
def at_instance():
    """
    Initialize and yield an instance of the AllTickets class.
    """
    at: AllTickets = AllTickets(
        api_url_root=API_URL_ROOT, auth_tuple=AUTH_TUPLE, page_size=25
    )
    yield at


@pytest.fixture()
def urls():
    """
    Provide commonly used mock Zendesk API urls.
    """
    class URLs:
        page_1_init: str = "https://zccsammdu.zendesk.com/api/v2/tickets.json?page[size]=25"
        page_1_linked: str = "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUm9BQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25"
        page_0_empty: str = "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25"
        page_2: str = "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25"

    yield URLs


@pytest.fixture()
def resp():
    """
    Provide test responses from the Zendesk API.
    """
    class Responses:
        alltickets_p0_empty: dict = {
            "tickets": [],
            "meta": {
                "has_more": False,
                "after_cursor": None,
                "before_cursor": None
            },
            "links": {
                "prev": None,
                "next": None
            }
        }

        alltickets_p1: dict = {
            "tickets": [
                {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5},
                {"id": 6}, {"id": 7}, {"id": 8}, {"id": 9}, {"id": 10},
                {"id": 11}, {"id": 12}, {"id": 13}, {"id": 14}, {"id": 15},
                {"id": 16}, {"id": 17}, {"id": 18}, {"id": 19}, {"id": 20},
                {"id": 21}, {"id": 22}, {"id": 23}, {"id": 24}, {"id": 25}
            ],
            "meta": {
                "has_more": True,
                "after_cursor": "eyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ==",
                "before_cursor": "eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ=="
            },
            "links": {
                "prev": "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25",
                "next": "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25"
            }
        }

        alltickets_p2: dict = {
            "tickets": [
                {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5},
                {"id": 6}, {"id": 7}, {"id": 8}, {"id": 9}, {"id": 10},
                {"id": 11}, {"id": 12}, {"id": 13}, {"id": 14}, {"id": 15},
                {"id": 16}, {"id": 17}, {"id": 18}, {"id": 19}, {"id": 20},
                {"id": 21}, {"id": 22}, {"id": 23}, {"id": 24}, {"id": 25}
            ],
            "meta": {
                "has_more": True,
                "after_cursor": "eyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ==",
                "before_cursor": "eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ=="
            },
            "links": {
                "prev": "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUm9BQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25",
                "next": "https://zccsammdu.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhVElBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25"
            }
        }

        common_404: dict = {
            "error": "RecordNotFound",
            "description": "Not found"
        }

    yield Responses


def test_init(at_instance):
    """
    Test the __init__() method, make sure it records the correct information.
    """
    assert at_instance.api_url_root == API_URL_ROOT
    assert at_instance.auth_tuple == AUTH_TUPLE
    assert at_instance.page_size == 25
    assert at_instance._url_curr == API_URL_ROOT + '/tickets.json?page[size]=25'
    assert at_instance._url_next == ''
    assert at_instance._url_prev == ''


def test_request_tickets_success(at_instance, urls, resp, requests_mock):
    """
    Test the _request_tickets() method, make sure it returns the correct data upon a
    successful call.
    """
    requests_mock.get(urls.page_1_init, json=resp.alltickets_p1)
    response: dict = at_instance._request_tickets(urls.page_1_init)

    assert response == resp.alltickets_p1


def test_request_tickets_failure_404(at_instance, urls, resp, requests_mock):
    """
    Test the _request_tickets() method, make sure it returns {} upon a 404 HTTP error.
    """
    requests_mock.get(urls.page_1_init, json=resp.common_404, status_code=404)
    response: dict = at_instance._request_tickets(urls.page_1_init)

    assert response == {}


def test_get_current_batch_success(at_instance, urls, resp, requests_mock):
    """
    Test the get_current_batch() method, make sure it returns the correct data upon a
    successful call.
    """
    requests_mock.get(urls.page_1_init, json=resp.alltickets_p1)
    current_batch: dict = at_instance.get_current_batch()

    assert current_batch == resp.alltickets_p1["tickets"]


def test_get_current_batch_failure_404(at_instance, urls, resp, requests_mock):
    """
    Test the get_current_batch() method, make sure make sure it returns [] upon a 404 HTTP
    error.
    """
    requests_mock.get(urls.page_1_init, json=resp.common_404, status_code=404)
    current_batch: dict = at_instance.get_current_batch()

    assert current_batch == []


def test_seek_batch_next_success(at_instance, urls, resp, requests_mock):
    """
    Test the seek_batch() method, ask to fetch the next batch, it should contain a new
    batch of tickets, therefore should return the correct data.
    """
    # call get_current_batch() to set up self.url_next
    requests_mock.get(urls.page_1_init, json=resp.alltickets_p1)
    at_instance.get_current_batch()

    requests_mock.get(urls.page_2, json=resp.alltickets_p2)
    next_batch: dict = at_instance.seek_batch("next")

    assert next_batch == resp.alltickets_p2


def test_seek_batch_prev_empty(at_instance, urls, resp, requests_mock):
    """
    Test the seek_batch() method, ask to fetch the previous batch, it should contain no
    tickets, therefore should return {}.
    """
    # call get_current_batch() to set up self.url_prev
    requests_mock.get(urls.page_1_init, json=resp.alltickets_p1)
    at_instance.get_current_batch()

    requests_mock.get(urls.page_0_empty, json=resp.alltickets_p0_empty)
    prev_batch: dict = at_instance.seek_batch("prev")

    assert prev_batch == {}


def test_goto_next_batch(at_instance, urls, resp, requests_mock):
    """
    Test the goto_next_batch() method, check that it modifies URL pointers correctly and
    returns the correct mock data.
    """
    # call get_current_batch() to set up self.url_next
    requests_mock.get(urls.page_1_init, json=resp.alltickets_p1)
    at_instance.get_current_batch()

    requests_mock.get(urls.page_2, json=resp.alltickets_p2)
    next_batch_list: list = at_instance.goto_next_batch()

    assert at_instance._url_prev == urls.page_1_init
    assert at_instance._url_curr == urls.page_2
    assert at_instance._url_next == resp.alltickets_p2["links"]["next"]

    assert next_batch_list == resp.alltickets_p2["tickets"]


def test_goto_prev_batch(at_instance, urls, resp, requests_mock):
    """
    Test the goto_prev_batch() method, check that it does not modify any URL pointers,
    because the mock previous batch is empty, and it returns [] correctly.
    """
    # call get_current_batch() to set up self.url_prev
    requests_mock.get(urls.page_1_init, json=resp.alltickets_p1)
    at_instance.get_current_batch()

    requests_mock.get(urls.page_0_empty, json=resp.alltickets_p0_empty)
    prev_batch_list: list = at_instance.goto_prev_batch()

    assert at_instance._url_prev == urls.page_0_empty
    assert at_instance._url_curr == urls.page_1_init
    assert at_instance._url_next == urls.page_2

    assert prev_batch_list == []
