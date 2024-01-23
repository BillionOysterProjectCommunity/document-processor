import os.path

import pandas as pd

from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import credentials_from_session

from markupsafe import Markup

from flask import (
    Flask, 
    request, 
    redirect, 
    render_template,
    session, 
    url_for
)
from theia.document.processor import DocumentProcessor
from theia.web.forms import MetadataForm
from theia.web.middleware import login_required
from theia.models.metadata import MetaData
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
    # contains description of the site plus url to login page
    if 'oauth_state' in session:
        return redirect(url_for('dashboard'))

    return render_template("index.html")

@app.route("/dashboard", methods=('GET', 'POST'))
@login_required
def dashboard():
    # contains logout button and url to form page
    return render_template("dashboard.html")
        
@app.route("/form", methods=('GET', 'POST'))
@login_required
def form():

    form = MetadataForm()

    if form.validate_on_submit():
        # TODO Add columns O-X from Ambassador Data Entry Google Sheet        

        rectangle_tag = form.tag_type.data
        round_tag = form.tag_type.data
        monitoring_date = form.monitoring_date.data
        total_live_oysters = form.total_live_oysters.data
        file = form.image.data
        path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        file.save(path)

        document_processor = DocumentProcessor(config)
        df = document_processor.process_document(path)
        df = df.dropna() # Drop corrupted values

        # Drive.process_ors_document(path)

        metadata = MetaData()
        broodstock = metadata.get_broodstock()
        set_date = metadata.get_setDate()
        distribution_date = metadata.get_distributionDate()

        df = pd.DataFrame({
            "Round Tag": round_tag,
            "Rectangle Tag": rectangle_tag,
            "Invalid": False,
            "Data_Quality": False,
            "Data_Sheet": "https://drive.google.com",
            "Data_Decisions": False,
            "Monitoring_Date": monitoring_date,
            "Broodstock": broodstock,
            "Set_Date": set_date,
            "Distribution_Date": distribution_date,
            "Clump": False,
            "Live_Oysters_Clump": False,
            "Total_Number_Live_Oysters": total_live_oysters,
            # TODO Continue to add fields
            "shell_height_mm":  df['measurements'],
            "live/dead": df['live/dead']
        })

        df = Markup(df.to_html())

        return render_template("result.html", df=df)
    
    return render_template("form.html", form=form)

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