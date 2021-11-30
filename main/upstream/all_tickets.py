#!/usr/bin/env python3.9
"""
Fetch all tickets from the Zendesk API for a given Zendesk account.

Public methods:
    - AllTickets(api_url_root: str, auth_tuple: tuple[str, str], page_size: int = 25)
    - AllTickets.get_current_batch() -> list
    - AllTickets.seek_batch(direction: str) -> dict  # direction in {"prev", "next"}
    - AllTickets.goto_next_batch() -> list
    - AllTickets.goto_prev_batch() -> list
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
    ) -> None:
        """
        Save Zendesk API URL root in a string and authentication info in a tuple.
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
        unsuccessful). Return an empty dict upon failure.
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
            print(f'---\n{e}\n---')

        return {}

    def get_current_batch(self) -> list:
        """
        Attempt to fetch the current batch of tickets, determined by `self._url_curr`.
        Update the next and previous URL pointers upon successful request.
        Return an empty dict if unsuccessful.
        """
        # attemp to fetch the current batch of tickets
        current_batch: dict = self._request_tickets(self._url_curr)

        if current_batch != {}:
            # update the URL pointers
            self._url_next = current_batch["links"]["next"]
            self._url_prev = current_batch["links"]["prev"]
            return current_batch["tickets"]

        return []

    def seek_batch(self, direction) -> dict:
        """
        Fetch an return either the previous or the next batch of tickets determined by the
        `direction` parameter, and do NOT modify the URL pointers.
        If the relevant URL pointers are unset, or if the specified batch of tickets are
        unavailable, return an empty dict.
        """
        assert direction in {"prev", "next"}

        # set the URL to that of the specified batch
        url: str
        if direction == "prev":
            url = self._url_prev
        else:
            url = self._url_next

        # if the URL pointer is non-empty for the specified direction
        if url:
            # attemp to fetch the specified batch of tickets
            batch: dict = self._request_tickets(url)

            # if the specified batch is available, then return the batch of tickets
            if batch and batch["tickets"] != []:
                return batch

        # otherwise return an empty dictionary
        return {}

    def goto_next_batch(self) -> list:
        """
        Attempt to fetch and return a list of the next batch of tickets.
        If successful, update the current, next, and previous URL pointers.
        Return an empty list if unsuccessful.
        """
        # attemp to fetch the next batch of tickets
        next_batch: dict = self.seek_batch("next")

        # if the next batch legitimately exists
        if next_batch != {} and next_batch["tickets"] != []:
            # update the URL pointers
            self._url_prev = self._url_curr
            self._url_curr = self._url_next
            self._url_next = next_batch["links"]["next"]
            # and return the next batch of tickets
            return next_batch["tickets"]

        return []

    def goto_prev_batch(self) -> list:
        """
        Attempt to fetch and return a list of the previous batch of tickets.
        If successful, update the current, next, and previous URL pointers.
        Return an empty list if unsuccessful.
        """

        # attemp to fetch the previous batch of tickets
        prev_batch: dict = self.seek_batch("prev")

        # if the previous batch legitimately exists
        if prev_batch != {} and prev_batch["tickets"] != []:
            # update the URL pointers
            self._url_next = self._url_curr
            self._url_curr = self._url_prev
            self._url_prev = prev_batch["links"]["prev"]
            # and return the previous batch of tickets
            return prev_batch["tickets"]

        return []
