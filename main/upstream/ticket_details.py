#!/usr/bin/env python3.9
"""
Fetch a ticket with associated user info from the Zendesk API for a given Zendesk account.

Public methods:
    - TicketDetails(api_url_root: str, auth_tuple: tuple[str, str])
    - TicketDetails.get_ticket(url) -> dict
"""

import requests


class TicketDetails:
    """
    A class that implements methods for fetching a single ticket from a given Zendesk
    account. Includes the ability to fetch user info as well.
    """

    def __init__(self, api_url_root: str, auth_tuple: tuple[str, str]) -> None:
        """
        Save Zendesk API URL root in a string and authentication info in a tuple.
        """
        self.api_url_root: str = api_url_root
        self.auth_tuple: tuple[str, str] = auth_tuple

    def _request_ticket(self, url) -> dict:
        """
        Request a ticket from the Zendesk API at the specified URL. Return the
        JSON results as a dict. Raise a RuntimeError if the HTTP response is not 200 (thus
        unsuccessful). Return an empty dict upon failure.
        """
        try:
            # assemble the request URL and perform the GET request
            response = requests.get(url, auth=self.auth_tuple)
            # handle when HTTP request is unsuccessful
            if response.status_code != 200:
                raise RuntimeError(
                    f"""
                    Failed to fetch a ticket's details.
                    Status: {response.status_code}
                    URL: {url}
                    """
                )
            return response.json()['ticket']

        except Exception as e:
            print(f'---\n{e}\n---')

        return {}

    def _request_user(self, user_id) -> dict:
        """
        Request a user from the Zendesk API with the specified user_id. Return the
        JSON results as a dict. Raise a RuntimeError if the HTTP response is not 200 (thus
        unsuccessful). Return an empty dict upon failure.
        """
        try:
            # assemble the request URL and perform the GET request
            url: str = self.api_url_root + f'/users/{user_id}.json'
            response = requests.get(url, auth=self.auth_tuple)
            # handle when HTTP request is unsuccessful
            if response.status_code != 200:
                raise RuntimeError(
                    f"""
                    Failed to fetch user info for {user_id}.
                    Status: {response.status_code}
                    URL: {url}
                    """
                )
            return response.json()['user']

        except Exception as e:
            print(f'---\n{e}\n---')

        return {}

    def get_ticket(self, url) -> dict:
        """
        Attempt to fetch a Zendesk ticket based on the provided url. Additionally, attempt
        to fetch the associated requester and assignee user profiles, and include them in
        the return result.
        Return an empty dict if unsuccessful.
        """
        # attemp to fetch the specified ticket
        ticket_details: dict = self._request_ticket(url)
        if ticket_details != {}:
            # attempt to fetch the associated requester and assignee user profiles
            requester: dict = self._request_user(user_id=ticket_details['requester_id'])
            assignee: dict = self._request_user(user_id=ticket_details['assignee_id'])
            if requester != {} and assignee != {}:
                # append associated requester and assignee user profiles to ticket details
                ticket_details['requester'] = requester
                ticket_details['assignee'] = assignee
                return ticket_details
        return {}
