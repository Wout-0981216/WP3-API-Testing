from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
import json
from database_functions import *
from datetime import datetime


ervaringsdeskundige_blueprint = Blueprint('ervaringsdeskundige', __name__)



# this is instead of using middelwares, user should be authorized if he want to access his resourses (onderzoek, orginistie )
def is_authenticated(): 
    return True if  "evd" in session else False
# user should not have access to the resourses of other users, exp: he can not retrive or update any research that not belong to him
def gereigisteerde_onderzoek_belong_to_evd (onderzoed_id):
   if is_authenticated():
       gergesteerde_onderzoek = get_gere_onderzoek_by_evd_id(session['evd']["id"])
       for go in gergesteerde_onderzoek: 
          if go["onderzoek_id"] == onderzoed_id: 
            return True
       return False   
   else:
      False
          



@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/onderzoek_overzicht', methods=['GET'])
def ervaringsdeskundige_onderzoek_overzicht():
    if  is_authenticated(): 
     return render_template('onderzoek_overzicht.html')
    else:
     return render_template('login_evd.html')


@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/haal_onderzoek/<status>', methods=['GET'])
def haal_onderzoek(status):
    # check if status is valie 
    if is_authenticated(): 
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
    else: 
       return render_template('login_evd.html')

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/inschrijven_onderzoek', methods=['PUT', 'POST'])
def inschrijven_onderzoek_route():
     # TO DO get beheereder_id 
     # TO DO implementeer ervaringsdeskundige AUTH en beheereder
    if is_authenticated():
     inschrijven_onderzoek(session['evd']["id"], request.json["id"], 1, 'geregisteered', datetime.now() )
     return jsonify(request.json)
    else: return render_template('login_evd.html')

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
   return render_template('ervaringsdeskundige_view_account.html',evd=evd, beperkingen=beperkingen)