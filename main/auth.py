from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database_functions import *


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    correct = beheerder_login(request.form)
    if correct:
        return redirect(url_for('auth.registration'))
    else:
        flash("Login onjuist")
        return render_template('login_beheerder.html')


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


@auth_blueprint.route("/login-beheerder", methods=['GET', 'POST'])
def login_beheerder():
        if request.method == 'POST':
            connection = get_db()
            cursor = connection.cursor()
            name = request.form['gebruikersnaamBh']
            password = request.form['wachtwoordBh']
            query = "SELECT * FROM beheerder WHERE gebruikersnaam = ?"
            cursor.execute(query, (name,))
            user_data = cursor.fetchone()

            if user_data is None or user_data['wachtwoord'] != password:
                flash('Foutieve gebruikersnaam/wachtwoord')
                return render_template('login_beheerder.html')
            else:
                is_admin = user_data['is_admin']
                session['role'] = is_admin
                session['beheerder_id'] = user_data['id']
                session['display_name'] = user_data['voornaam']
                return redirect(url_for('auth.login_evd', is_admin=is_admin))

        return render_template('login_beheerder.html')


@auth_blueprint.route("/login-ervaringsdeskundige", methods=['GET', 'POST'])
def login_evd():
    if request.method == 'POST':
        connection = get_db()
        cursor = connection.cursor()
        name = request.form['gebruikersnaamEvd']
        password = request.form['wachtwoordEvd']
        query = "SELECT * FROM ervaringsdeskundige WHERE gebruikersnaam = ?"
        cursor.execute(query, (name,))
        user_data = cursor.fetchone()

        if user_data is None or user_data['wachtwoord'] != password:
            flash('Foutieve gebruikersnaam/wachtwoord')
            return render_template('login_evd.html')
        else:
            session['beheerder_id'] = user_data['id']
            session['display_name'] = user_data['voornaam']
            return redirect(url_for('auth.login_beheerder'))

    return render_template('login_evd.html')

@auth_blueprint.route("/ervaringsdeskundige_overzicht", methods=['GET', 'POST'])
def evd_overzicht():
    all_evd = get_all_evd_from_database()
    return render_template('ervaringsdeskundige_overzicht.html', all_evd=all_evd)

@auth_blueprint.route("/ervaringsdeskundige_goedkeuren/<evd_id>", methods=['GET', 'POST'])
def confirm_evd(evd_id):
    confirm_evd_status(evd_id)
    return redirect(url_for('auth.evd_overzicht'))

@auth_blueprint.route("/ervaringsdeskundige_afkeuren/<evd_id>", methods=['GET', 'POST'])
def deny_evd(evd_id):
    deny_evd_status(evd_id)
    return redirect(url_for('auth.evd_overzicht'))

@auth_blueprint.route("/ervaringsdeskundige_view/<evd_id>", methods=['GET', 'POST'])
def view_evd(evd_id):
    evd_info = get_evd_from_database_by_id(evd_id)
    return render_template('view_ervaringsdeskundige.html', evd_info = evd_info)