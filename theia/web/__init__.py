import os
from flask import Flask

import theia
from theia.settings.config import Config

def create_app():
    app = Flask(__name__)
    app.config["SETTINGS"] = Config()
    
    iam_credentials = app.config["SETTINGS"].read('iam-file-name')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(theia.__file__) + "/" + iam_credentials
    app.secret_key = app.config["SETTINGS"].read('flask-secret-key')
    
    if app.config["SETTINGS"].read('debug') == True:
        app.config["SETTINGS"].set('redirect-uri', "https://127.0.0.1:8080/callback")

    from theia.web.views.auth import a # auth
    from theia.web.views.dashboard import dash # dashbboard
    from theia.web.views.form import entry # forms

    app.register_blueprint(a)
    app.register_blueprint(dash)
    app.register_blueprint(entry)

    return app