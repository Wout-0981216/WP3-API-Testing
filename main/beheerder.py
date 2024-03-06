from flask import Blueprint, render_template, jsonify
from database_functions import get_aanvragen, get_onderzoeken, get_evd


beheerder_blueprint = Blueprint('beheerder', __name__)

@beheerder_blueprint.route('/beheerder', methods=['GET'])
def beheerder():
    aanvragen_data = get_aanvragen()
    return render_template('beheerder_overzicht.html', aanvragen=aanvragen_data)

@beheerder_blueprint.route('/get_aanvragen', methods=['GET'])
def get_aanvragen_route():
    aanvragen = get_aanvragen()
    return jsonify({'aanvragen': aanvragen})

@beheerder_blueprint.route('/get_onderzoeken', methods=['GET'])
def get_onderzoeken_route():
    onderzoeken = get_onderzoeken()
    return jsonify({'onderzoeken': onderzoeken})

@beheerder_blueprint.route('/get_evd', methods=['GET'])
def get_evder_route():
    evd = get_evd()
    return jsonify({'evd': evd})
