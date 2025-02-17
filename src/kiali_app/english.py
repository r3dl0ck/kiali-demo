from flask import Flask, request
import requests
import os
import logging
import argparse

logger = logging.getLogger(__name__)

# English App
english_app = Flask(__name__)

def hello():
    return "Hello World!"

@english_app.route("/")
def english_hello():
    return hello()

@english_app.route("/chained")
def english_chained():
    try:
        logger.debug(f"Spanish service: {SPANISH_SVC}")
        spanish_response = requests.get(SPANISH_SVC)
        spanish_message = spanish_response.text
        logger.debug(f"Received response from Spanish service: {spanish_message}")
        return f"{hello()} -> {spanish_message}"
    except requests.exceptions.RequestException as e:
        logger.exception("Error connecting to Spanish service")
        return f"Error connecting to Spanish service: {e}", 500


def main() -> None:
    parser = argparse.ArgumentParser(description='English Flask App')
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

    parser.add_argument('--spanish-svc', dest='spanish_svc', type=str,
                        default='http://spanish:8080/chained',
                        help='Spanish service URL')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.log_level)
    logger.info(f"English service starting up with Spanish service URL: {args.spanish_svc}")

    global SPANISH_SVC
    SPANISH_SVC = args.spanish_svc


    english_app.run(port=args.flask_port, debug=args.flask_debug, use_reloader=False)