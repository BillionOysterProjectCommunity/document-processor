from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from theia.web.forms import (
    AddUserForm,
    DeleteUserForm
)
from theia.web.middleware import login_required, admin_required

def whitelist(google):
    # check if r.content contains an email present within the firestore database
    return True

admin = Blueprint(
    'admin', 
    __name__, 
    url_prefix='/admin',
    template_folder="templates"
    )

@admin.route("/manage", methods=('GET', 'POST'))
@login_required
@admin_required
def manage():

    # GCP Project only has one default database so no database has to be supplied upon client initialization
    db = firestore.Client()
    user_ref = db.collection("users")
    user_ref.document()
    users = [u.to_dict() for u in user_ref.stream()]
    # have two seperate views for adding and deleting users

    return render_template("admin.html", users=users)

@admin.route("/delete/user/<string:user_email>", methods=('GET', 'POST'))
@login_required
def delete_user(user_email: str):

    form = DeleteUserForm()
    if form.validate_on_submit():
        db = firestore.Client()
        user_ref = db.collection("users")
        docs = list(user_ref.where(filter=FieldFilter("email", "==", user_email)).stream())
        try:
            user_id = docs[0].id
            user_ref.document(user_id).delete()

            return redirect(url_for("admin.manage"))
        except IndexError:
            return redirect(url_for("admin.manage"))
    
    return render_template("admin-delete-user.html", user_email=user_email, form=form)

@admin.route("/add/user", methods=('GET', 'POST'))
@login_required
def add_user():

    form = AddUserForm()
    if form.validate_on_submit():
        db = firestore.Client()
        user_ref = db.collection("users")
        user_ref.add({
            "email": form.email.data,
            "roles": form.roles.data
        })
        return redirect(url_for("admin.manage"))

    return render_template("admin-add-user.html", form=form)