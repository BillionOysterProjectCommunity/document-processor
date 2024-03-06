from flask import (
    Flask, 
    Blueprint,
    current_app,
    request, 
    redirect, 
    render_template,
    session, 
    url_for
)

from theia.settings.config import Config

from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

config = Config()

client_id = config.read('oauth-client-id')
client_secret = config.read('oauth-client-secret')
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'

BASE_URI = "https://127.0.0.1:8080"
REDIRECT_URI = f"{BASE_URI}/callback"

SCOPE = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive.metadata.readonly", "openid"]

a = Blueprint(
    'a', 
    __name__, 
    url_prefix='/',
    template_folder="templates"
    )

@a.route("/login")
def login():
    google = OAuth2Session(client_id, 
                           scope=SCOPE, 
                           redirect_uri=REDIRECT_URI)

    authorization_url, state = google.authorization_url(authorization_base_url)
    session['oauth_state'] = state

    return redirect(authorization_url)

@a.route("/callback")
def callback():
    google = OAuth2Session(client_id, state=request.args.get('state'), redirect_uri=REDIRECT_URI)
    token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for("dash.dashboard"))

@a.route("/", methods=('GET', 'POST'))
def index():
    if 'oauth_state' in session:
        return redirect(url_for('dash.dashboard'))

    return render_template("index.html")

@a.route("/logout")
def logout():
    del session['oauth_state']
    del session['oauth_token']

    return redirect(url_for("a.index"))