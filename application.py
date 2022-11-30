from hello_world import hello
import os
from flask import Flask, jsonify, Response, render_template, request

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        endpoint = os.environ['API_ENDPOINT']
    except KeyError:
        endpoint = 'Local'
    return hello(environment=endpoint)


if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)