import json

from functools import wraps

from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from flask import (
    Flask, 
    request, 
    redirect, 
    render_template,
    session, 
    url_for
)

from theia.settings.config import config

def is_valid_session():
        client_id = config(key='oauth-client-id')
        try:
                google = OAuth2Session(client_id, token=session['oauth_token'])
                cred = credentials_from_session(google)
        except ValueError:
                False
        return True

def login_required(f):
    @wraps(f)
    def required(*args, **kwargs):
        if 'oauth_state' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return required

def admin_required(f):
    @wraps(f)
    def required(*args, **kwargs):
        
        db = firestore.Client()

        google = OAuth2Session(config(key='oauth-client-id'), token=session['oauth_token'])
        r = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
        info = json.loads(r.content)

        user_ref = db.collection("users")
        present = list(user_ref.where(filter=FieldFilter("email", "==", info['email'])).stream())

        try:
            user_id = present[0].id
            user = user_ref.document(user_id).get().to_dict()
            if "admin" not in user['roles']:
                return redirect(url_for("dash.dashboard"))
        except IndexError:
            return redirect(url_for("dash.dashboard"))
        return f(*args, **kwargs)
    return required