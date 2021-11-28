#!/usr/bin/env python3.9
"""
Main application entry point. Serves the root ('/') endpoint.
"""

import secrets
import json
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
    """
    Render the main view on the frontend.
    Generate a unique session_id if it does not exist.
    Initialize an AllTickets object to be used during the session.
    """
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
        return_batch: list = ticket_objs[session['session_id']].goto_prev_batch()
    elif direction == 'next':
        return_batch: list = ticket_objs[session['session_id']].goto_next_batch()
    else:
        return make_response("'direction' must either be 'prev' or 'next'!", 400)

    print(return_batch)

    # display error for empty result
    if not return_batch:
        return make_response(f"Failed to fetch the {direction} page.", 404)
    else:
        return jsonify(return_batch)


@app.route('/ticket_details', methods=['GET'])
def ticket_details():
    """
    """
    # only permit access after a session has been established
    if 'session_id' not in session:
        return make_response("Do not access this endpoint directly!", 403)

    # obtain the url of the ticket
    ticket_url = request.args.get('ticket_url')
    print(f"\n{ticket_url}\n")

    ticket: dict = json.loads("""
{"ticket":{"url":"https://zccsammdu.zendesk.com/api/v2/tickets/2.json","id":2,"external_id":null,"via":{"channel":"api","source":{"from":{},"to":{},"rel":null}},"created_at":"2021-11-27T07:00:17Z","updated_at":"2021-11-28T03:59:12Z","type":null,"subject":"velit eiusmod reprehenderit officia cupidatat","raw_subject":"velit eiusmod reprehenderit officia cupidatat","description":"Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.Aliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.","priority":null,"status":"pending","recipient":null,"requester_id":1910383993885,"submitter_id":1910383993885,"assignee_id":1910383993885,"organization_id":1500634551141,"group_id":4411226980499,"collaborator_ids":[],"follower_ids":[],"email_cc_ids":[],"forum_topic_id":null,"problem_id":null,"has_incidents":false,"is_public":true,"due_at":null,"tags":["est","incididunt","nisi"],"custom_fields":[],"satisfaction_rating":null,"sharing_agreement_ids":[],"fields":[],"followup_ids":[],"ticket_form_id":1500003309421,"brand_id":1500002344441,"allow_channelback":false,"allow_attachments":true}}
    """)["ticket"]

    return render_template('ticket_details.html', selected_ticket=ticket)
