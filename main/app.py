#!/usr/bin/env python3.9
"""
Main application entry point. Serves the following endpoints:
    - GET /
    - GET /navigate         direction=      navigation direction, either "prev" or "next"
    - GET /ticket_details   ticket_url=     URL of the ticket whose details are requested
"""

import secrets
from flask import Flask, render_template, request, make_response, jsonify, session

from main.upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE
from main.upstream.all_tickets import AllTickets
from main.upstream.ticket_details import TicketDetails


app = Flask(__name__)

# configure session cookie for Flask
app.secret_key = secrets.token_urlsafe(nbytes=64)
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"

# keep track of the AllTickets objects and TicketDetails objects for each session in
# memory; each object is identified by a unique session_id
allticket_objs: dict = {}
ticketdetails_objs: dict = {}


@app.route('/', methods=['GET'])
def index():
    """
    Render the main view on the frontend.
    Generate a unique session_id if it does not exist.
    Initialize an AllTickets object to be used during the session.
    """
    # if a session_id is not found for this session
    if 'session_id' not in session:
        # generate a unique session id
        session['session_id'] = secrets.token_urlsafe(nbytes=64)

        # initialize a new AllTickets object for this session and store in allticket_objs
        allticket_objs[session['session_id']] = AllTickets(
            api_url_root=API_URL_ROOT,
            auth_tuple=AUTH_TUPLE,
            page_size=25
        )

    return render_template('index.html', all_tickets=allticket_objs[session['session_id']])


@app.route('/navigate', methods=['GET'])
def navigate():
    """
    Upon request, navigate to the previous or next batch of tickets within the session's
    corresponding AllTickets object.
    Do not permit access to this endpoint without an existing session.
    """
    # only permit access after a session has been established
    if 'session_id' not in session:
        return make_response("Do not access this endpoint directly!", 403)

    # navigate to the specified batch of tickets
    direction: str = request.args.get('direction')
    if direction == 'prev':
        return_batch: list = allticket_objs[session['session_id']].goto_prev_batch()
    elif direction == 'next':
        return_batch: list = allticket_objs[session['session_id']].goto_next_batch()
    else:
        return make_response("'direction' must either be 'prev' or 'next'!", 400)

    # display an error for empty result; if successful, return the navigated batch
    if not return_batch:
        return make_response(f"Failed to fetch the {direction} page.", 404)
    else:
        return jsonify(return_batch)


@app.route('/ticket_details', methods=['GET'])
def ticket_details():
    """
    Upon request, generate a TicketDetails object for the user's session if it does not
    exist, fetch the details of the requested ticket as well as its associated users by
    the given ticket URL using the TicketDetails get_ticket() method. Render the pop-up
    modal HTML with the ticket and user details, and retrun it to the frontend.
    Do not permit access to this endpoint without an existing session.
    """
    # only permit access after a session has been established
    if 'session_id' not in session:
        return make_response("Do not access this endpoint directly!", 403)

    # if the session does not have an associated TicketDetails objects, initialize one
    if session['session_id'] not in ticketdetails_objs:
        ticketdetails_objs[session['session_id']] = TicketDetails(
            api_url_root=API_URL_ROOT,
            auth_tuple=AUTH_TUPLE,
        )

    # obtain the provided url of the ticket
    ticket_url = request.args.get('ticket_url')

    # fetch the ticket's details with associated user information
    ticket: dict = ticketdetails_objs[session['session_id']].get_ticket(ticket_url)

    return render_template('ticket_details.html', ticket=ticket)
