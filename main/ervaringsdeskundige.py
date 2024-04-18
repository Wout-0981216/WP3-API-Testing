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

def geregisteerde_onderzoek_belong_to_evd (onderzoed_id):
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
    if  status == 'beschikbaar':
      beschikbaarOnderzoeken = get_onderzoek(session["evd"])
      geregisteeredOnderzoek = get_geregisteered_onderzoek(session['evd']["id"], status)
      # uitsluiten van geregisteeredOnderzoek
      ids_to_exclude = {obj["id"] for obj in geregisteeredOnderzoek}
      result = [obj for obj in beschikbaarOnderzoeken if obj["id"] not in ids_to_exclude]
      return jsonify(result)
    else: 
      onderzoeken = get_geregisteered_onderzoek(session['evd']["id"], status)
      return jsonify(onderzoeken)

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/inschrijven_onderzoek', methods=['PUT', 'POST'])
def inschrijven_onderzoek_route():
    inschrijven_onderzoek(session['evd']["id"], request.json["id"], None, 'nieuw', None )
    return jsonify(request.json)

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/uitschrijven_onderzoek', methods=['PUT', 'POST'])
def uitschrijven_onderzoek_route():
    if geregisteerde_onderzoek_belong_to_evd(request.json['id']):  
        uitschrijven_onderzoek(request.json['id'])
        return jsonify(request.json)
    else: return render_template('login_evd.html')

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/account_overzicht', methods=['GET', 'POST'])
def view_account_details():
   evd = get_evd_from_database_by_id(session['evd']['id'])
   beperkingen = get_beperkingen_from_database_by_evd_id(session['evd']['id'])
   return render_template('ervaringsdeskundige_view_account.html',evd=evd, beperkingen=beperkingen)