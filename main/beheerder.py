from flask import Blueprint, render_template, jsonify
from database_functions import get_aanvragen


beheerder_blueprint = Blueprint('beheerder', __name__)

@beheerder_blueprint.route('/beheerder', methods=['GET'])
def beheerder():
    aanvragen_data = get_aanvragen()
    return render_template('beheerder_overzicht.html', aanvragen=aanvragen_data)

@beheerder_blueprint.route('/get_aanvragen', methods=['GET'])
def get_aanvragen_route():
    aanvragen = get_aanvragen()
    return jsonify({'aanvragen': aanvragen})
