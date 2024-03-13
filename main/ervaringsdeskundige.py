from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
import json
from database_functions import get_onderzoek, insert_dom_data,get_geregisteered_onderzoek, inschrijven_onderzoek, uitschrijven_onderzoek, get_onderzoek_by_id
from datetime import datetime


ervaringsdeskundige_blueprint = Blueprint('ervaringsdeskundige', __name__)



@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/onderzoek_overzicht', methods=['GET'])
def ervaringsdeskundige_onderzoek_overzicht():
    return render_template('onderzoek_overzicht.html')

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/haal_beschikbaar_onderzoek', methods=['GET', 'POST'])
def haal_beschikbaar_onderzoek():
    # insert_dom_data()
    beschikbaarOnderzoeks = get_onderzoek({'beschikbaar':True})
    geregisteeredOnderzoek = get_geregisteered_onderzoek({'ervaringsdeskundige_id':1})
    # uitsluiten van geregisteeredOnderzoek
    ids_to_exclude = {obj["id"] for obj in geregisteeredOnderzoek}
    result = [obj for obj in beschikbaarOnderzoeks if obj["id"] not in ids_to_exclude]
    return jsonify(result)
  
    


@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/haal_geregisteered_onderzoek', methods=['GET', 'POST'])
def haal_geregisteered_onderzoek():
    # Ik kan niet ervaringsdeskundige login vinden
    
    # Check voor AUTH
    # if 'beheerder_id' in session:
        
    #  geregisteeredOnderzoeks = get_geregisteered_onderzoek({'ervaringsdeskundige_id':session['beheerder_id']})
     
    #  return jsonify(geregisteeredOnderzoeks)
    # else:
    #  return 'Not Authenticated'
    geregisteeredOnderzoeks = get_geregisteered_onderzoek({'ervaringsdeskundige_id':1})
    return jsonify(geregisteeredOnderzoeks)

    




@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/inschrijven_onderzoek', methods=['PUT', 'POST'])
def inschrijven_onderzoek_route():
     # TO DO implementeer ervaringsdeskundige AUTH en beheereder
    inschrijven_onderzoek(1, request.json["id"], 1, 'nieuw', datetime.now() )
    
    return jsonify(request.json)

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/uitschrijven_onderzoek', methods=['PUT', 'POST'])
def uitschrijven_onderzoek_route():
    
        onderzoek = get_onderzoek_by_id(request.json['id'])
        if onderzoek is not None:
            uitschrijven_onderzoek(request.json['id'])
            return jsonify(request.json)
    
        else:
            return ('Onderzoek not found')

  
    