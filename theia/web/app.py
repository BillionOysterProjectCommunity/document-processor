from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

from flask import Flask, request, redirect, session, url_for

from theia.drive.client import Client as Drive
from theia.settings.config import Config

config = Config()

client_id = config.read('oauth-client-id')
client_secret = config.read('oauth-client-secret')
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'

BASE_URI = "https://127.0.0.1:8080"
REDIRECT_URI = f"{BASE_URI}/callback"

app = Flask(__name__)
app.secret_key = config.read('flask-secret-key')

@app.route("/login")
def login():
    google = OAuth2Session(client_id, 
                           scope="https://www.googleapis.com/auth/drive.metadata.readonly", 
                           redirect_uri=REDIRECT_URI)

    authorization_url, state = google.authorization_url(authorization_base_url)
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route("/callback")
def callback():
    google = OAuth2Session(client_id, state=request.args.get('state'), redirect_uri=REDIRECT_URI)
    token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for(".index"))

@app.route("/")
def index():
    
    return (f"""
            <a href={request.url}>{request.url}</a>
            <div></div>
            <a href=/login>login</a>
            <a href=/drive>drive</a>
            """
            )

@app.route("/drive")
def drive():

    google = OAuth2Session(client_id, token=session['oauth_token'])
    cred = credentials_from_session(google)

    drive = Drive(credentials=cred, config=Config())

    return drive.show_initial_files()

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')