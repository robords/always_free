from hello_world import hello
import os
import git
from flask import Flask, jsonify, Response, render_template, request

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        endpoint = os.environ['API_ENDPOINT']
    except KeyError:
        endpoint = 'Local?'
    return hello(environment=endpoint)

@application.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo()
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)
