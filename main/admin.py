from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database_functions import *


admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin')
def admin_page():
    return render_template('admin.html')