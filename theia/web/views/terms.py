from flask import Blueprint, request, redirect, render_template, session, url_for

import json

from theia.settings.config import config

t = Blueprint("t", __name__, url_prefix="/terms", template_folder="templates")

@t.route("/privacy")
def privacy():
    return render_template("privacy.html")