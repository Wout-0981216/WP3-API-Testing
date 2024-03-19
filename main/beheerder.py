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

@beheerder_blueprint.route("/ervaringsdeskundige_goedkeuren", methods=['GET', 'POST'])
def all_evd_to_be_confirmed():
    all_evd_to_confirm = get_evd_from_database_by_status_nieuw()
    return render_template('ervaringsdeskundige_goedkeuren.html', all_evd_to_confirm=all_evd_to_confirm)

@beheerder_blueprint.route("/ervaringsdeskundige_goedkeuren/<evd_id>", methods=['GET', 'POST'])
def confirm_evd(evd_id):
    confirm_evd_status(evd_id)
    return redirect(url_for('beheerder.all_evd_to_be_confirmed'))

@beheerder_blueprint.route("/ervaringsdeskundige_afkeuren/<evd_id>", methods=['GET', 'POST'])
def deny_evd(evd_id):
    deny_evd_status(evd_id)
    return redirect(url_for('beheerder.all_evd_to_be_confirmed'))

@beheerder_blueprint.route("/ervaringsdeskundige_view/<evd_id>", methods=['GET', 'POST'])
def view_evd(evd_id):
    evd_info = get_evd_from_database_by_id(evd_id)
    return render_template('view_ervaringsdeskundige.html', evd_info=evd_info)

@beheerder_blueprint.route("/ervaringsdeskundige_inschrijving", methods=['GET', 'POST'])
def view_evd_inschrijving():
    inschrijvingen = get_inschrijvingen_op_onderzoeken()
    return render_template('inschrijvingen.html', inschrijvingen=inschrijvingen)

@beheerder_blueprint.route("/onderzoek_view/<onderzoek_id>", methods=['GET', 'POST'])
def view_onderzoek(onderzoek_id):
    onderzoek_info = get_onderzoek_by_id(onderzoek_id)
    return render_template('view_onderzoek.html', onderzoek_info=onderzoek_info)

@beheerder_blueprint.route("/ervaringsdeskundige_overzicht", methods=['GET', 'POST'])
def evd_overzicht():
    all_evd = get_all_evd_from_database()
    return render_template("ervaringsdeskundige_overzicht.html", all_evd=all_evd)