from hello_world import hello
import os
import git
from flask import Flask, jsonify, Response, render_template, request

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        # this will work if it's on AWS EB
        endpoint = os.environ['API_ENDPOINT']
    except KeyError:
        try:
            # this will work if we're on pythonanywhere
            if os.environ['PYTHONANYWHERE_SITE'] == 'www.pythonanywhere.com':
                endpoint = 'Hosted on Python Anywhere'
        except KeyError:
            endpoint = 'Local'
    return render_template('index.html', environment=endpoint)

@application.route('/update_server', methods=['POST'])
def webhook():
    # based on: https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664
    if request.method == 'POST':
        # finding the right way to specify the local git repo is a pain
        # https://stackoverflow.com/questions/22081209/find-the-root-of-the-git-repository-where-the-file-lives
        repo = git.Repo('~/always_free') 
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)
