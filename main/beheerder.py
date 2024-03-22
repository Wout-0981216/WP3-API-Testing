from flask import Blueprint, render_template, redirect, url_for, jsonify, flash, session
from database_functions import *


beheerder_blueprint = Blueprint('beheerder', __name__)

@beheerder_blueprint.before_request
def before_beheerder_request():
    if 'beheerder_id' in session:
        return
    flash('U bent niet bevoegd deze pagina te bekijken')
    return redirect(url_for('auth.index'))

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
    flash('Ervaringsdeskundige succesvol goedgekeurd!', 'success')
    return redirect(url_for('beheerder.all_evd_to_be_confirmed'))


@beheerder_blueprint.route("/ervaringsdeskundige_afkeuren/<evd_id>", methods=['GET', 'POST'])
def deny_evd(evd_id):
    deny_evd_status(evd_id)
    flash('Ervaringsdeskundige succesvol afgekeurd!', 'success')
    return redirect(url_for('beheerder.all_evd_to_be_confirmed'))


@beheerder_blueprint.route("/ervaringsdeskundige_goedkeuren/no_redirect/<evd_id>", methods=['GET', 'POST'])
def confirm_evd_no_redirect(evd_id):
    confirm_evd_status(evd_id)
    flash('Ervaringsdeskundige succesvol goedgekeurd!', 'success')
    return redirect(url_for('beheerder.evd_overzicht'))


@beheerder_blueprint.route("/ervaringsdeskundige_afkeuren/no_redirect/<evd_id>", methods=['GET', 'POST'])
def deny_evd_no_redirect(evd_id):
    deny_evd_status(evd_id)
    flash('Ervaringsdeskundige succesvol afgekeurd!', 'success')
    return redirect(url_for('beheerder.evd_overzicht'))


@beheerder_blueprint.route("/ervaringsdeskundige_overzicht", methods=['GET', 'POST'])
def evd_overzicht():
    all_evd = get_all_evd_from_database()
    return render_template("ervaringsdeskundige_overzicht.html", all_evd=all_evd)


@beheerder_blueprint.route("/ervaringsdeskundige_view/<evd_id>", methods=['GET', 'POST'])
def view_evd(evd_id):
    evd_info = get_evd_from_database_by_id(evd_id)
    return render_template('view_ervaringsdeskundige.html', evd_info=evd_info)


@beheerder_blueprint.route("/ervaringsdeskundige_inschrijving", methods=['GET', 'POST'])
def view_evd_inschrijving():
    inschrijvingen = get_inschrijvingen_op_onderzoeken()
    return render_template('inschrijvingen.html', inschrijvingen=inschrijvingen)


@beheerder_blueprint.route("/ervaringsdeskundige_all_inschrijvingen", methods=['GET', 'POST'])
def view_all_evd_inschrijving():
    alle_inschrijvingen = get_alle_inschrijvingen_op_onderzoeken()
    return render_template('Alle_inschrijvingen.html', alle_inschrijvingen=alle_inschrijvingen)


@beheerder_blueprint.route("/onderzoek_view/<onderzoek_id>", methods=['GET', 'POST'])
def view_onderzoek(onderzoek_id):
    onderzoek_info = get_onderzoek_by_id(onderzoek_id)
    return render_template('view_onderzoek.html', onderzoek_info=onderzoek_info)


@beheerder_blueprint.route("/onderzoeken", methods=['GET', 'POST'])
def onderzoeken():
    nieuwe_onderzoeken = get_new_onderzoeken()
    return render_template('onderzoeken.html', nieuwe_onderzoeken=nieuwe_onderzoeken)


@beheerder_blueprint.route("/alle_onderzoeken", methods=['GET', 'POST'])
def view_alle_onderzoeken():
    alle_onderzoeken = get_all_onderzoeken()
    return render_template('alle_onderzoeken.html', alle_onderzoeken=alle_onderzoeken)


@beheerder_blueprint.route("/onderzoek_goedkeuren/<id>", methods=['GET', 'POST'])
def confirm_onderzoek(id):
    confirm_onderzoek_status(id)
    flash('Onderzoek succesvol goedgekeurd!', 'success')
    return redirect(url_for('beheerder.onderzoeken'))


@beheerder_blueprint.route("/onderzoek_afkeuren/<id>", methods=['GET', 'POST'])
def deny_onderzoek(id):
    deny_onderzoek_status(id)
    flash('Onderzoek succesvol afgekeurd!', 'success')
    return redirect(url_for('beheerder.onderzoeken'))


@beheerder_blueprint.route("/onderzoek_goedkeuren_no_redirect/<id>", methods=['GET', 'POST'])
def confirm_onderzoek_no_redirect(id):
    confirm_onderzoek_status(id)
    flash('Onderzoek succesvol goedgekeurd!', 'success')
    return redirect(url_for('beheerder.view_alle_onderzoeken'))


@beheerder_blueprint.route("/onderzoek_afkeuren_no_redirect/<id>", methods=['GET', 'POST'])
def deny_onderzoek_no_redirect(id):
    deny_onderzoek_status(id)
    flash('Onderzoek succesvol afgekeurd!', 'success')
    return redirect(url_for('beheerder.view_alle_onderzoeken'))


@beheerder_blueprint.route("/inschrijving_goedkeuren/<onderzoek_id>", methods=['GET', 'POST'])
def confirm_inschrijving(onderzoek_id):
    confirm_inschrijving_status(onderzoek_id)
    flash('Inschrijving succesvol goedgekeurd!', 'success')
    return redirect(url_for('beheerder.view_evd_inschrijving'))


@beheerder_blueprint.route("/inschrijving_afkeuren<onderzoek_id>", methods=['GET', 'POST'])
def deny_inschrijving(onderzoek_id):
    deny_inschrijving_status(onderzoek_id)
    flash('Inschrijving succesvol afgekeurd!', 'success')
    return redirect(url_for('beheerder.view_evd_inschrijving'))


@beheerder_blueprint.route("/inschrijving_goedkeuren_no_redirect/<onderzoek_id>", methods=['GET', 'POST'])
def confirm_inschrijving_no_redirect(onderzoek_id):
    confirm_inschrijving_status(onderzoek_id)
    flash('Inschrijving succesvol goedgekeurd!', 'success')
    return redirect(url_for('beheerder.view_all_evd_inschrijving'))


@beheerder_blueprint.route("/inschrijving_afkeuren_no_redirect/<onderzoek_id>", methods=['GET', 'POST'])
def deny_inschrijving_no_redirect(onderzoek_id):
    deny_inschrijving_status(onderzoek_id)
    flash('Inschrijving succesvol afgekeurd!', 'success')
    return redirect(url_for('beheerder.view_all_evd_inschrijving'))
