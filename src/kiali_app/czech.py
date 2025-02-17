from flask import Flask, request
import requests
import os
import logging
import argparse

logger = logging.getLogger(__name__)

# Czech App
czech_app = Flask(__name__)

@czech_app.route("/")
def czech_hello():
    return "Ahoj světe!"

def main() -> None:
    parser = argparse.ArgumentParser(description='Czech Flask App')
    parser.add_argument('--flask-debug', dest='flask_debug', action='store_true',
                        help='Enable Flask debug mode')
    parser.add_argument('--no-flask-debug', dest='flask_debug', action='store_false',
                        help='Disable Flask debug mode')
    parser.set_defaults(flask_debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])

    parser.add_argument('--flask-port', dest='flask_port', type=int,
                        default=int(os.getenv('FLASK_PORT', 8080)),
                        help='Port to run Flask app on')

    parser.add_argument('--log-level', dest='log_level', type=str,
                        default=os.getenv('LOG_LEVEL', 'INFO').upper(),
                        help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.log_level)

    czech_app.run(port=args.flask_port, debug=args.flask_debug, use_reloader=False)