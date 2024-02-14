from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database_functions import insert_ervaringsdeskundige_into_database, select_type_beperkingen_from_database, select_beperking_from_database_by_type


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
    beperking_typen = select_type_beperkingen_from_database()
    beperking_dict = {}
    for beperking_typen in beperking_typen:
        beperkingen = select_beperking_from_database_by_type(beperking_typen[0])
        beperking_dict[beperking_typen] = beperkingen
 
    return render_template('register.html', beperking_dict=beperking_dict)

@auth_blueprint.route("/registration", methods=['POST'])
def add_registration():
    msg = insert_ervaringsdeskundige_into_database(request.form)
    flash(msg)
    return redirect(url_for("auth.registration"))
