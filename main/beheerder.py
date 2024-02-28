from flask import Blueprint, render_template


beheerder_blueprint = Blueprint('beheerder', __name__)

@beheerder_blueprint.route('/beheerder')
def beheerder():
    return render_template('beheerder_overzicht.html')