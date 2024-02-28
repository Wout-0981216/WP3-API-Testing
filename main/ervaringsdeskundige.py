from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
import json



ervaringsdeskundige_blueprint = Blueprint('ervaringsdeskundige', __name__)


# Serveer hier alle html's en bestanden 
@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/onderzoek_overzicht', methods=['GET'])
def ervaringsdeskundige_onderzoek_overzicht():
   
    return render_template('onderzoek_overzicht.html')

@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/haal_beschikbaar_onderzoek', methods=['GET', 'POST'])
def haal_beschikbaar_onderzoek():
    #TO DO (Die de dadtabase heeft gemaakt) Maak een functie die het beschikbaar "gebaseerde criteria" onderzoek retourneert

    with open("C:/Users/Alaa Alkatlabe/PycharmProjects/wp3-2024-rest-1e4-kingcode/dom.json", "r") as file: 
        data = json.load(file)
    return jsonify(data)
    # return render_template('onderzoek_overzicht.html')
    


@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/haal_geregisteered_onderzoek', methods=['GET', 'POST'])
def haal_geregisteered_onderzoek():
    #To-do (Die de dadtabase heeft gemaakt) Maak een functie die het beschikbare "gebaseerde criteria" onderzoek retourneert

    with open("C:/Users/Alaa Alkatlabe/Desktop/My lesen Hamza/3 taken finsh/wp3-2024-rest-1e4-kingcode/dom.json", "r") as file: 
        data = json.load(file)
    return jsonify(data)
    # return render_template('onderzoek_overzicht.html')




@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/deelnaam_onderzoek', methods=['PUT', 'POST'])
def deelnaam_onderzoek():
   # TO DO Creëer een functie die een individu registreert voor een onderzoek
  
    return jsonify(request.json)