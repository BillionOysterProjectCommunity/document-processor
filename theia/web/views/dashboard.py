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

from theia.web.middleware import login_required

dash = Blueprint(
    'dash', 
    __name__, 
    url_prefix='/d',
    template_folder="templates"
    )

@dash.route("/dashboard", methods=('GET', 'POST'))
@login_required
def dashboard():
    return render_template("dashboard.html")