from flask import Flask

from theia.settings.config import Config

def create_app():
    app = Flask(__name__)
    app.config["SETTINGS"] = Config()
    app.secret_key = app.config["SETTINGS"].read('flask-secret-key')
    app.config['UPLOAD_FOLDER'] = 'uploads'

    from theia.web.views.auth import a
    from theia.web.views.dashboard import dash
    from theia.web.views.form import entry

    app.register_blueprint(a)
    app.register_blueprint(dash)
    app.register_blueprint(entry)

    return app