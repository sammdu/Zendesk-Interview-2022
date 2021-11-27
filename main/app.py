#!/usr/bin/env python3.9
"""
Main application entry point. Serves the root ('/') endpoint.
"""

from flask import Flask, render_template, request, make_response, jsonify
from upstream.zendesk_common import API_URL_ROOT, AUTH_TUPLE


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
