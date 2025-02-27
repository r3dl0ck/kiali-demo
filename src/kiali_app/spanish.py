from flask import Flask, request
import requests
import os
import logging
import argparse

logger = logging.getLogger(__name__)

# Spanish App
spanish_app = Flask(__name__)

def hello():
    return "Hello Mundo!"

@spanish_app.route("/health")
def health():
    return "Healthy\n"

@spanish_app.route("/")
def spanish_hello():
    return hello()

@spanish_app.route("/chained")
def spanish_chained():
    try:
        logger.debug(f"Czech service: {czech_svc}")
        czech_response = requests.get(czech_svc, timeout=timeout)
        czech_response.raise_for_status()
        czech_message = czech_response.text
        logger.debug(f"Received response from Czech service: {czech_message}")
        return f"{hello()} -> {czech_message}"
    except requests.exceptions.Timeout:
        logger.info('Request timed out.')
        return f"Operation timed out after {timeout}s", 408
    except requests.exceptions.HTTPError as e:
        logger.exception(f"HTTP error connecting to Czech service: {e}")
        return f"HTTP error connecting to Czech service: {e}", 500
    except requests.exceptions.RequestException as e:
        logger.exception("Error connecting to Czech service")
        return f"Error connecting to Czech service: {e}", 500


def main() -> None:
    parser = argparse.ArgumentParser(description='Spanish Flask App')
    parser.add_argument('--flask-debug', dest='flask_debug', action='store_true',
                        help='Enable Flask debug mode')
    parser.add_argument('--no-flask-debug', dest='flask_debug', action='store_false',
                        help='Disable Flask debug mode')
    parser.set_defaults(flask_debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])

    parser.add_argument('--flask-port', dest='flask_port', type=int,
                        default=int(os.getenv('FLASK_PORT', 8080)),
                        help='Port to run Flask app on')

    parser.add_argument('--timeout', dest='timeout', type=int,
                        default=int(os.getenv('TIMEOUT', 5)),
                        help='Timeout for requests to other services')

    parser.add_argument('--host', dest='host', type=str,
                        default='0.0.0.0',
                        help='Host IP to listen on')

    parser.add_argument('--log-level', dest='log_level', type=str,
                        default=os.getenv('LOG_LEVEL', 'INFO').upper(),
                        help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    parser.add_argument('--czech-svc', dest='czech_svc', type=str,
                        default='http://czech:8080/',
                        help='Czech service URL')

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.log_level)
    logger.info(f"Spanish service starting up with Czech service URL: {args.czech_svc}, timeout: {args.timeout}")

    global czech_svc
    global timeout
    czech_svc = args.czech_svc
    timeout = args.timeout


    spanish_app.run(host=args.host, port=args.flask_port, debug=args.flask_debug, use_reloader=False)