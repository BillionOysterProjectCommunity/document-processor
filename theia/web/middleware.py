import json

from functools import wraps

from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from flask import Flask, request, redirect, render_template, session, url_for

from theia.settings.config import config


def is_valid_session():
    client_id = config(key="oauth-client-id")
    try:
        google = OAuth2Session(client_id, token=session["oauth_token"])
        cred = credentials_from_session(google)
    except ValueError:
        False
    return True


def login_required(f):
    @wraps(f)
    def required(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return required


def admin_required(f):
    @wraps(f)
    def required(*args, **kwargs):

        user = session["user"]

        if "admin" not in user["roles"]:
            return redirect(url_for("dash.dashboard"))
        return f(*args, **kwargs)

    return required
