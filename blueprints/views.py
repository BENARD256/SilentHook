from flask import render_template, Blueprint

from blueprints.auth import auth_bp

#   Views Page Rendering
#https://share.google/aimode/FwSnRw7tgrAZqYRHA


# General Blueprint 
views_bp = Blueprint('views', __name__)


# AUTHENTICATION

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('/auth/register.html') # Flask auto checks in templates


@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    return render_template('/auth/login.html')


# DASHBOARD
@views_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('/dashboard/dashboard.html')