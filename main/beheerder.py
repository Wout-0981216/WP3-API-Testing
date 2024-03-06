from flask import Blueprint, render_template, redirect, url_for, jsonify
from database_functions import *


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

@beheerder_blueprint.route("/ervaringsdeskundige_overzicht", methods=['GET', 'POST'])
def evd_overzicht():
    all_evd = get_all_evd_from_database()
    return render_template('ervaringsdeskundige_overzicht.html', all_evd=all_evd)

@beheerder_blueprint.route("/ervaringsdeskundige_goedkeuren/<evd_id>", methods=['GET', 'POST'])
def confirm_evd(evd_id):
    confirm_evd_status(evd_id)
    return redirect(url_for('beheerder.evd_overzicht'))

@beheerder_blueprint.route("/ervaringsdeskundige_afkeuren/<evd_id>", methods=['GET', 'POST'])
def deny_evd(evd_id):
    deny_evd_status(evd_id)
    return redirect(url_for('beheerder.evd_overzicht'))

@beheerder_blueprint.route("/ervaringsdeskundige_view/<evd_id>", methods=['GET', 'POST'])
def view_evd(evd_id):
    evd_info = get_evd_from_database_by_id(evd_id)
    return render_template('view_ervaringsdeskundige.html', evd_info = evd_info)
