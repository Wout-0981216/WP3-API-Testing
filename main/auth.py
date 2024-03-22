from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database_functions import *


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/', methods=['GET', 'POST'])
def index():
    # create_beheerder()
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
    beperking_typen = select_type_beperkingen_from_database()
    beperking_dict = {}
    for beperking_typen in beperking_typen:
        beperkingen = select_beperking_from_database_by_type(beperking_typen[0])
        beperking_dict[beperking_typen] = beperkingen

    msg = insert_ervaringsdeskundige_into_database(request.form, beperking_dict)
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
                return redirect(url_for('beheerder.beheerder', is_admin=is_admin))

        return render_template('login_beheerder.html')


# @auth_blueprint.route("/login-ervaringsdeskundige", methods=['GET', 'POST'])
# def login_evd():
#     if request.method == 'POST':
#         connection = get_db()
#         cursor = connection.cursor()
#         name = request.form['gebruikersnaamEvd']
#         password = request.form['wachtwoordEvd']
#         query = "SELECT * FROM ervaringsdeskundige WHERE gebruikersnaam = ?"
#         cursor.execute(query, (name,))
#         user_data = cursor.fetchone()

#         if user_data is None or user_data['wachtwoord'] != password:
#             flash('Foutieve gebruikersnaam/wachtwoord')
#             return render_template('login_evd.html')
#         else:
#             session['beheerder_id'] = user_data['id']
#             session['display_name'] = user_data['voornaam']
#             return redirect(url_for('auth.login_beheerder'))

#     return render_template('login_evd.html')


# @auth_blueprint.route("/login-ervaringsdeskundige", methods=['GET', 'POST'])
# def login_evd():
#     return render_template('login_evd.html')

#         if user_data is None or user_data['wachtwoord'] != password:
#             flash('Foutieve gebruikersnaam/wachtwoord')
#             return render_template('login_evd.html')
#         else:
#             session['beheerder_id'] = user_data['id']
#             session['display_name'] = user_data['voornaam']
#             return redirect(url_for('ervaringsdeskundige.ervaringsdeskundige_onderzoek_overzicht'))

@auth_blueprint.route("/login-ervaringsdeskundige", methods=['GET', 'POST'])
def login_evd():
    return render_template('login_evd.html')


@auth_blueprint.route("/login-ervaringsdeskundige-new", methods=['POST'])
def login_evd_new(): 
     gebruikersnaam = request.form['gebruikersnaamEvd']  if request.form is not None and   request.form['gebruikersnaamEvd'] is not None  else  request.json['gebruikersnaamEvd'] if request.json  is not None and request.json['gebruikersnaamEvd']  is not None else None
     wachtwoordEvd = request.form['wachtwoordEvd']  if request.form is not None and  request.form['wachtwoordEvd'] is not None  else  request.json['wachtwoordEvd'] if request.json  is not None and request.json['wachtwoordEvd']  is not None else None
     print({wachtwoordEvd:wachtwoordEvd, gebruikersnaam: gebruikersnaam})
     if user_exist(gebruikersnaam,  wachtwoordEvd):
      evd = get_evd_by_username(gebruikersnaam)
      # problem with the database please hash the password
      del evd["wachtwoord"]
      session['evd'] = evd
      return redirect('/ervaringsdeskundige/onderzoek_overzicht')
     else:
      return render_template('login_evd.html')
     