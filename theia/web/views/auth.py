from flask import (
    Blueprint,
    request, 
    redirect, 
    render_template,
    session, 
    url_for
)

import json

from theia.web.views.admin import whitelist

from theia.settings.config import config

from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

SCOPE = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email", 
    "https://www.googleapis.com/auth/userinfo.profile"
]

a = Blueprint(
    'a', 
    __name__, 
    url_prefix='/',
    template_folder="templates"
    )

@a.route("/login")
def login():

    client_id = config(key='oauth-client-id')
    authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'

    google = OAuth2Session(client_id, 
                           scope=SCOPE, 
                           redirect_uri=config('redirect-uri'))

    authorization_url, state = google.authorization_url(authorization_base_url)
    session['oauth_state'] = state

    return redirect(authorization_url)

@a.route("/callback")
def callback():

    client_id = config(key='oauth-client-id')
    client_secret = config(key='oauth-client-secret')
    token_url = 'https://accounts.google.com/o/oauth2/token'

    google = OAuth2Session(client_id, state=request.args.get('state'), redirect_uri=config('redirect-uri'))
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