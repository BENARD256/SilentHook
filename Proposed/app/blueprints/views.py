from flask import render_template, Blueprint

#from blueprints.auth import auth_bp
#from blueprints.triggers import triggers_bp

from app.blueprints.auth import auth_bp # Importing Auth Blueprint for Page Routes
from app.blueprints.triggers import triggers_bp # Importing Triggers Blueprint for Page Routes
from app.extensions import db # Importing the database instance from extensions

#   Views Page Rendering
#https://share.google/aimode/FwSnRw7tgrAZqYRHA


# General Blueprint 
views_bp = Blueprint('views', __name__)


# AUTHENTICATION

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('/auth/register.html') # Flask auto checks in templates


# Login / Index Page

@auth_bp.route('/login',methods=['GET', 'POST'])
@views_bp.route('/', methods=['GET', 'POST'])
def login():
    return render_template('/auth/login.html')


# DASHBOARD
@views_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('/dashboard/dashboard.html')


# User's Baits

@views_bp.route("/triggers", methods=['GET', 'POST'])
def user_triggers():
    return render_template('/triggers/triggers.html')

# Alerts Page
@views_bp.route("/alerts", methods=['GET', 'POST'])
def alerts():
    return render_template('alerts/alerts.html')

# About Page
@views_bp.route("/docs", methods=['GET', 'POST'])
def about():
    return render_template('/about/about.html')
