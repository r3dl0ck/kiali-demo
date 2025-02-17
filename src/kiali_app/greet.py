from flask import Flask, request
import requests
import os
import logging
import argparse

# Main Greeting API App
greet_api_app = Flask(__name__)

@greet_api_app.route("/")
def greet_all():
    try:
        czech_response = requests.get(CZECH_SVC)
        czech_message = czech_response.text
    except requests.exceptions.RequestException as e:
        czech_message = f"Error connecting to Czech service: {e}"

    try:
        english_response = requests.get(ENGLISH_SVC)
        english_message = english_response.text
    except requests.exceptions.RequestException as e:
        english_message = f"Error connecting to English service: {e}"

    try:
        spanish_response = requests.get(SPANISH_SVC)
        spanish_message = spanish_response.text
    except requests.exceptions.RequestException as e:
        spanish_message = f"Error connecting to Spanish service: {e}"

    return f"Greet app: {english_message} | {spanish_message} | {czech_message}\n"

@greet_api_app.route("/chained")
def greet_chained():
    try:
       english_response = requests.get(ENGLISH_SVC + "chained")  # Call chained English
       english_message = english_response.text

       return f"Chained: {english_message}\n"

    except requests.exceptions.RequestException as e:
        return f"Error connecting to services: {e}", 500


def main() -> None:
    parser = argparse.ArgumentParser(description='Greet API Flask App')
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
                        default='http://spanish:8080/',
                        help='Spanish service URL')

    parser.add_argument('--english-svc', dest='english_svc', type=str,
                        default='http://english:8080/',
                        help='English service URL')

    parser.add_argument('--czech-svc', dest='czech_svc', type=str,
                        default='http://czech:8080/',
                        help='Czech service URL')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting: spanish_svc={args.spanish_svc}, english_svc={args.english_svc}, czech_svc={args.czech_svc}")

    global SPANISH_SVC
    global ENGLISH_SVC
    global CZECH_SVC

    SPANISH_SVC = args.spanish_svc
    ENGLISH_SVC = args.english_svc
    CZECH_SVC = args.czech_svc

    greet_api_app.run(port=args.flask_port, debug=args.flask_debug, use_reloader=False)