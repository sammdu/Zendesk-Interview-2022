#!/usr/bin/env python3.9
"""
Main application entry point. Serves the root ('/') endpoint.
"""

import secrets
from flask import Flask, render_template, request, make_response, jsonify, session

from main.upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE
from main.upstream.all_tickets import AllTickets


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(nbytes=64)
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"

# keep track of the AllTickets objects for each session in memory;
# each AllTickets object is identified by a unique session_id
ticket_objs: dict = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    # if a session_id is not found for this session
    if 'session_id' not in session:
        # generate a unique session id
        session['session_id'] = secrets.token_urlsafe(nbytes=64)

        # initialize a new AllTickets object for this session and store in ticket_objs
        ticket_objs[session['session_id']] = AllTickets(
            api_url_root=API_URL_ROOT,
            auth_tuple=AUTH_TUPLE,
            page_size=25
        )

    return render_template('index.html', all_tickets=ticket_objs[session['session_id']])


@app.route('/navigate', methods=['GET'])
def navigate():
    if 'session_id' not in session:
        return make_response("Do not access this endpoint directly!", 403)

    direction: str = request.args.get('direction')
    if direction == 'prev':
        return jsonify(ticket_objs[session['session_id']].goto_prev_batch())
    elif direction == 'next':
        return jsonify(ticket_objs[session['session_id']].goto_next_batch())
    else:
        return make_response("'direction' must either be 'prev' or 'next'!", 400)
