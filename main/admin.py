from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database_functions import *


admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.before_request
def before_admin_request():
    if 'beheerder_id' in session:
        if session['role'] == 1:
            return
    flash('U bent niet bevoegd deze pagina te bekijken')
    return redirect(url_for('auth.index'))

@admin_blueprint.route('/admin')
def admin_page():
    return render_template('admin.html')