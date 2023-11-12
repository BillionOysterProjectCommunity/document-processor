import os.path

from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

from flask import (
    Flask, 
    request, 
    redirect, 
    render_template,
    session, 
    url_for
)
from theia.document.processor import DocumentProcessor
from theia.drive.client import Client as Drive
from theia.settings.config import Config

config = Config()

client_id = config.read('oauth-client-id')
client_secret = config.read('oauth-client-secret')
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'

BASE_URI = "https://127.0.0.1:8080"
REDIRECT_URI = f"{BASE_URI}/callback"

SCOPE = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive.metadata.readonly"]

app = Flask(__name__)
app.secret_key = config.read('flask-secret-key')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/login")
def login():
    google = OAuth2Session(client_id, 
                           scope=SCOPE, 
                           redirect_uri=REDIRECT_URI)

    authorization_url, state = google.authorization_url(authorization_base_url)
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route("/logout")
def logout():
    del session['oauth_state']
    del session ['oauth_token']

    return redirect("/")

@app.route("/callback")
def callback():
    google = OAuth2Session(client_id, state=request.args.get('state'), redirect_uri=REDIRECT_URI)
    token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    session['oauth_token'] = token

    return redirect("/")

@app.route("/", methods=('GET', 'POST'))
def index():

    if request.method == 'POST':
        # Form submission processing for ors document and metadata

        # Todo Configure processing of multiple files
        file = request.files['file']
        path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        file.save(path)

        document_processor = DocumentProcessor(config)
        df = document_processor.process_document(path)
        df = df.dropna() # Drop corrupted values

        # Upload files to Google Drive

        google = OAuth2Session(client_id, token=session['oauth_token'])
        cred = credentials_from_session(google)

        drive = Drive(credentials=cred, config=Config())

        data_processed = True

        return render_template("index.html", authorized=True, df=df, data_processed = data_processed)

    if 'oauth_state' in session:
        return render_template("index.html", authorized=True)
    
    return render_template("index.html", authorized=False)

@app.route("/authorized")
def drive():

    if 'oauth_state' not in session:
        return {"authorized": False}

    google = OAuth2Session(client_id, token=session['oauth_token'])
    cred = credentials_from_session(google)

    drive = Drive(credentials=cred, config=Config())

    return {"authorized": True}

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')