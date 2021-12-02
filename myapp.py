from flask import Flask, request, jsonify, render_template, Response
import json
from time import sleep
from quali_api_wrapper import QualiApiSession

app = Flask(__name__)


def read_credentials(file_path: str):
    with open(file_path) as f_in:
        credentials = json.load(f_in)
    return credentials


def get_api():
    creds = read_credentials("credentials.json")
    return QualiApiSession(host=creds["cs_host"],
                           username=creds["cs_username"],
                           password=creds["cs_password"],
                           domain=creds["cs_domain"])


@app.route('/')
def home():
    api = get_api()
    suites = api.get_suite_templates()
    return render_template('index.html', domain=api.domain, suites=suites)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5051, debug=True)
