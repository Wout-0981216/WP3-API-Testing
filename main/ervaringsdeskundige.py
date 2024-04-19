from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
import json
from database_functions import *
from datetime import datetime


ervaringsdeskundige_blueprint = Blueprint('ervaringsdeskundige', __name__)


@ervaringsdeskundige_blueprint.before_request
def before_ervaringsdeskundige_request():
    if 'evd' in session:
            return
    flash('U bent niet bevoegd deze pagina te bekijken')
    return redirect(url_for('auth.index'))

def gereigisteerde_onderzoek_belong_to_evd (onderzoed_id):
    gergesteerde_onderzoek = get_gere_onderzoek_by_evd_id(session['evd']["id"])
    for go in gergesteerde_onderzoek: 
        if go["onderzoek_id"] == onderzoed_id: 
            return True
    return False



@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/onderzoek_overzicht', methods=['GET'])
def ervaringsdeskundige_onderzoek_overzicht():
    return render_template('onderzoek_overzicht.html')


@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/haal_onderzoek/<status>', methods=['GET'])
def haal_onderzoek(status):
    # check if status is valie 
    newStatus = 'beschikbaar' if status is None else str(status)
    if  newStatus == 'beschikbaar':
      beschikbaarOnderzoeks = get_onderzoek( session["evd"],{'beschikbaar':True})
      geregisteeredOnderzoek = get_geregisteered_onderzoek({'ervaringsdeskundige_id':session['evd']["id"] , 'status': 'beschikbaar'})
      # uitsluiten van geregisteeredOnderzoek
      ids_to_exclude = {obj["id"] for obj in geregisteeredOnderzoek}
      result = [obj for obj in beschikbaarOnderzoeks if obj["id"] not in ids_to_exclude]
      return jsonify(result)
    else: 
      onderzoeken = get_geregisteered_onderzoek({'ervaringsdeskundige_id':session['evd']["id"], 'status': newStatus})
      return jsonify(onderzoeken)

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/inschrijven_onderzoek', methods=['PUT', 'POST'])
def inschrijven_onderzoek_route():
    # TO DO get beheereder_id 
    # TO DO implementeer ervaringsdeskundige AUTH en beheereder
    inschrijven_onderzoek(session['evd']["id"], request.json["id"], 1, 'nieuw', datetime.now() )
    return jsonify(request.json)

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/uitschrijven_onderzoek', methods=['PUT', 'POST'])
def uitschrijven_onderzoek_route():
    # check if the evd has access to the registed resarch
    if gereigisteerde_onderzoek_belong_to_evd(request.json['id']):  
        uitschrijven_onderzoek(request.json['id'])
        return jsonify(request.json)
    else: return render_template('login_evd.html')


@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/account_overzicht', methods=['GET', 'POST'])
def view_account_details():
   evd = get_evd_from_database_by_id(session['evd']['id'])
   beperkingen = get_beperkingen_from_database_by_evd_id(session['evd']['id'])
   return render_template('ervaringsdeskundige_view_account.html', evd=evd, beperkingen=beperkingen)


@ervaringsdeskundige_blueprint.route("/update_account", methods=['GET'])
def update_account():
    evd = get_evd_from_database_by_id(session['evd']['id'])
    beperkingen = get_beperkingen_from_database_by_evd_id(session['evd']['id'])
    beperking_typen = select_type_beperkingen_from_database()
    beperking_dict = {}
    for beperking_typen in beperking_typen:
        beperkingen = select_beperking_from_database_by_type(beperking_typen[0])
        beperking_dict[beperking_typen] = beperkingen

    return render_template('edit_account.html', evd=evd, beperking_dict=beperking_dict, beperkingen=beperkingen)

@ervaringsdeskundige_blueprint.route("/update_account", methods=['POST'])
def update_account_post():
    voornaam = request.form.get('voornaam')
    achternaam = request.form.get('achternaam')
    postcode = request.form.get('postcode')
    geslacht = request.form.get('geslacht')
    gebruikersnaam = request.form.get('gebruikersnaam')
    telefoonnummer = request.form.get('telefoonnummer')
    geboortedatum = request.form.get('geboortedatum')
    gebruikte_hulpmiddel = request.form.get('gebruikte_hulpmiddel')
    bijzonderheden = request.form.get('Bijzonderheden')
    beperking_typen = select_type_beperkingen_from_database()
    beperking_dict = {}
    for beperking_typen in beperking_typen:
        beperkingen = select_beperking_from_database_by_type(beperking_typen[0])
        beperking_dict[beperking_typen] = beperkingen

    msg = update_account_in_database(voornaam, achternaam, postcode, geslacht, gebruikersnaam, telefoonnummer, geboortedatum, gebruikte_hulpmiddel, bijzonderheden, int(session["evd"]['id']), beperking_dict, request.form)

    flash(msg)

    return redirect(url_for("ervaringsdeskundige.view_account_details"))
