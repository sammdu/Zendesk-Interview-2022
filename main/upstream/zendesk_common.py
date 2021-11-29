#!/usr/bin/env python3.9
"""
Common components for the Zendesk API, configured via environment variables.
    - API_URL_ROOT: the URL root for Zendesk API requests
        * depends on environment variable ZENDESK_API_SUBDOMAIN
    - AUTH_TUPLE: HTTP Basic Authentication tuple, to be supplied to the requests library
        * depends on environment variables ZENDESK_API_EMAIL, ZENDESK_API_TOEKEN
"""

import os

# check for relevant environment variable ZENDESK_API_SUBDOMAIN
if not (subdomain := os.getenv("ZENDESK_API_SUBDOMAIN")):
    raise EnvironmentError("\tError: environment variable ZENDESK_API_SUBDOMAIN not set.")

# the Zendesk API root URL based on provided subdomain
API_URL_ROOT: str = f'https://{subdomain}.zendesk.com/api/v2'

# check for relevant environment variables ZENDESK_API_EMAIL, ZENDESK_API_TOEKEN
if not (email := os.getenv("ZENDESK_API_EMAIL")):
    raise EnvironmentError("\tError: environment variable ZENDESK_API_EMAIL not set.")
if not (token := os.getenv("ZENDESK_API_TOEKEN")):
    raise EnvironmentError("\tError: environment variable ZENDESK_API_TOEKEN not set.")

# HTTP basic authentication tuple, specificlly for the requests library
AUTH_TUPLE: tuple = (
    email + '/token',
    token,
)
