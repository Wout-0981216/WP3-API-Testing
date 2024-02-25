from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
import json



ervaringsdeskundige_blueprint = Blueprint('ervaringsdeskundige', __name__)


# Serveer hier alle html's en bestanden 
@ervaringsdeskundige_blueprint.route('/ervaringsdeskundige/onderzoek_overzicht', methods=['GET'])
def ervaringsdeskundige_onderzoek_overzicht():
   
    return render_template('onderzoek_overzicht.html')

