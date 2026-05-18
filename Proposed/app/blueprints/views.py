from flask import render_template, Blueprint, request
from flask_jwt_extended import verify_jwt_in_request

#from blueprints.auth import auth_bp
#from blueprints.triggers import triggers_bp

from app.blueprints.auth import auth_bp # Importing Auth Blueprint for Page Routes
from app.blueprints.triggers import triggers_bp # Importing Triggers Blueprint for Page Routes
from app.extensions import db # Importing the database instance from extensions
from flask import redirect, url_for # Importing redirect and url_for for handling redirects in views

#   Views Page Rendering
#https://share.google/aimode/FwSnRw7tgrAZqYRHA


# General Blueprint 
views_bp = Blueprint('views', __name__)
auth_page_bp = Blueprint('auth_page', __name__)# AUTHENTICATION


 

# Blueprint for Auth Page Routes
# This blueprint handles the rendering of authentication-related pages such as login and registration.
@auth_page_bp.route('/',            methods=['GET'])
@auth_page_bp.route('/auth/login',  methods=['GET'])
def login():
    return render_template('auth/login.html')

@auth_page_bp.route('/auth/register', methods=['GET'])
def register():
    return render_template('auth/register.html')

## dashboard page route

@views_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard/dashboard.html')


## Triggers Page Route 
@views_bp.route('/triggers', methods=['GET'])
def user_triggers():
    return render_template('triggers/triggers.html')

## Alerts Page Route
@views_bp.route('/alerts', methods=['GET'])
def alerts():
    return render_template('alerts/alerts.html')


## Docs Page Route

@views_bp.route('/docs', methods=['GET'])
def about():
    return render_template('about/about.html')


## Error Handlers for Auth Blueprint
@auth_page_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@auth_page_bp.app_errorhandler(401)
def handle_unauthorized(e):
    return redirect(url_for('auth_page.login'))