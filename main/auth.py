from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database_functions import insert_ervaringsdeskundige_into_database


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    flash("U bent succesvol uitgelogd")
    return redirect(url_for("auth.index"))

@auth_blueprint.route("/registration", methods=['GET'])
def registration():
    return render_template('register.html')

@auth_blueprint.route("/registration", methods=['POST'])
def add_registration():
    msg = insert_ervaringsdeskundige_into_database(request.form)
    flash(msg)
    return render_template('register.html')
