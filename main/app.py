#!/usr/bin/env python3.9
"""
Main application entry point. Serves the root ('/') endpoint.
"""

from flask import Flask, render_template, request, make_response, jsonify
from main.upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE
from main.upstream.all_tickets import AllTickets


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    a = AllTickets(
        api_url_root=API_URL_ROOT,
        auth_tuple=AUTH_TUPLE,
        page_size=25
    )
    return render_template('index.html', tickets=a.get_current_batch())
