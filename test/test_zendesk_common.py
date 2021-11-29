#!/usr/bin/env python3.9
"""

"""

import os
import pytest


@pytest.fixture()
def setup_and_teardown():
    """
    Set up dummy environment variables for testing, and remove them once testsing is
    complete.
    """
    # dummy environemnt variable values used for testing
    subdomain: str = 'pytest'
    email: str = 'pytest@example.com'
    token: str = 'pytest123'

    # set the dummy environemnt variable in the system
    print("\n> setup environment variables for testing")
    os.environ['ZENDESK_API_SUBDOMAIN'] = subdomain
    os.environ['ZENDESK_API_EMAIL'] = email
    os.environ['ZENDESK_API_TOEKEN'] = token

    # pass the dummy values to the test function
    yield subdomain, email, token

    # unset the dummy environemnt variable in the system
    print("\n> remove environment variables after testing")
    os.environ.pop('ZENDESK_API_SUBDOMAIN')
    os.environ.pop('ZENDESK_API_EMAIL')
    os.environ.pop('ZENDESK_API_TOEKEN')


def test_zendesk_common_constants(setup_and_teardown):
    """
    Import the relevant Zendesk configuration constants and see if they contain correct
    information based on the dummy environment variables
    """
    # retrieve dummy environment variable values
    subdomain, email, token = setup_and_teardown

    # import Zendesk constants being tested
    from main.upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE

    # create test conditions that need to be true
    cond_API_URL_ROOT: bool = API_URL_ROOT == f"https://{subdomain}.zendesk.com/api/v2"
    cond_AUTH_TUPLE: bool = AUTH_TUPLE == (f"{email}/token", token)

    assert cond_API_URL_ROOT and cond_AUTH_TUPLE
