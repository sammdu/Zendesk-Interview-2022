#!/usr/bin/env python3.9
"""
Runs a web server for this Flask project on http://127.0.0.1:5000/
"""

from main.app import app

if __name__ == '__main__':
    # run the Flask development server
    app.run(threaded=True, port=5000)
