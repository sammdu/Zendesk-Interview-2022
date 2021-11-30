#!/usr/bin/env python3.9
"""
Test the `zendesk_common.py` file under main/upstream.
"""

import os
import pytest


@pytest.fixture()
def variables():
    """
    Retrieve environment variables for testing, and pass their values to the test
    functions.
    """
    # get environemnt variable values for testing
    subdomain: str = os.getenv("ZENDESK_API_SUBDOMAIN")
    email: str = os.getenv("ZENDESK_API_EMAIL")
    token: str = os.getenv("ZENDESK_API_TOEKEN")

    # pass the values to the test function
    yield subdomain, email, token


def test_zendesk_common_url_root(variables):
    """
    Import the relevant Zendesk configuration constants and see if it contains the correct
    URL root.
    """
    subdomain, email, token = variables

    from main.upstream.zendesk_common import API_URL_ROOT
    assert API_URL_ROOT == f"https://{subdomain}.zendesk.com/api/v2"


def test_zendesk_common_auth(variables):
    """
    Import the relevant Zendesk configuration constants and see if it contains the correct
    authentication tuple.
    """
    subdomain, email, token = variables

    from main.upstream.zendesk_common import AUTH_TUPLE
    assert AUTH_TUPLE == (f"{email}/token", token)
