#!/usr/bin/env python3.9
"""
Functions related to fetching all tickets from the Zendesk API.
"""

import requests


class AllTickets:
    """
    A class that implements methods for fetching all tickets for a given Zendesk account.
    """

    def __init__(
        self,
        api_url_root: str,
        auth_tuple: tuple[str, str],
        page_size: int = 25
    ):
        """
        Accept an integer `page_size` parameter, and configure the number of tickets to be
        retrieved per batch of tickets. Also configure the initial request URL and
        initialize the previous and next page request URLs to be empty strings ''.
        """
        self.api_url_root: str = api_url_root
        self.auth_tuple: tuple[str, str] = auth_tuple
        self.page_size: int = page_size
        self._url_curr: str = self.api_url_root + f'/tickets.json?page[size]={page_size}'
        self._url_next: str = ''
        self._url_prev: str = ''

    def _request_tickets(self, url) -> dict:
        """
        Request a batch of tickets from the Zendesk API at the specified URL. Return the
        JSON results as a dict. Raise a RuntimeError if the HTTP response is not 200 (thus
        unsuccessful).
        """
        try:
            # assemble the request URL and perform the GET request
            response = requests.get(url, auth=self.auth_tuple)
            # handle when HTTP request is unsuccessful
            if response.status_code != 200:
                raise RuntimeError(
                    f"""
                    Failed to fetch a batch of tickets.
                    Status: {response.status_code}
                    URL: {url}
                    """
                )
            return response.json()

        except Exception as e:
            print(f'\n---\n{e}\n---\n')

        return {}

    def get_current_batch(self) -> dict:
        """
        Attempt to fetch the current batch of tickets, determined by `self._url_curr`.
        Update the next and previous URL pointers upon successful request.
        Return an empty dict if unsuccessful.
        """
        current_batch: dict = self._request_tickets(self._url_curr)
        if current_batch != {}:
            self._url_next = current_batch["links"]["next"]
            self._url_prev = current_batch["links"]["prev"]
            return current_batch["tickets"]
        return {}

    def get_next_batch(self) -> dict:
        """
        Attempt to fetch the next batch of tickets, determined by `self._url_next`.
        Update the current, next, and previous URL pointers upon successful request.
        Return an empty dict if unsuccessful.
        """
        if self._url_next:
            # attemp to fetch the next batch of tickets
            next_batch: dict = self._request_tickets(self._url_next)
            if next_batch != {} and next_batch["tickets"] != []:
                # update URL pointers if the next batch legitimately exists
                self._url_prev = self._url_curr
                self._url_curr = self._url_next
                self._url_next = next_batch["links"]["next"]
                return next_batch["tickets"]
        return {}

    def get_prev_batch(self) -> dict:
        """
        Attempt to fetch the previous batch of tickets, determined by `self._url_prev`.
        Update the current, next, and previous URL pointers upon successful request.
        Return an empty dict if unsuccessful.
        """
        if self._url_prev:
            # attemp to fetch the previous batch of tickets
            prev_batch: dict = self._request_tickets(self._url_prev)
            if prev_batch != {} and prev_batch["tickets"] != []:
                # update URL pointers if the next batch legitimately exists
                self._url_next = self._url_curr
                self._url_curr = self._url_prev
                self._url_prev = prev_batch["links"]["prev"]
                return prev_batch["tickets"]
        return {}
