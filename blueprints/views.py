from flask import render_template, Blueprint, send_from_directory, after_this_request # Delete Bait After its Served

from flask_jwt_extended import jwt_required # Require JWT to download bait

from blueprints.auth import auth_bp
from blueprints.triggers import triggers_bp
import os


# General Blueprint 
views_bp = Blueprint('views', __name__)


# AUTHENTICATION

@auth_bp.route('/register', methods=['GET'])
@views_bp.route('/register', methods=['GET'])
def register():
    return render_template('/auth/register.html') # Flask auto checks in templates


# Login / Index Page

@auth_bp.route('/login',methods=['GET']) # /auth
@views_bp.route('/', methods=['GET'])
@views_bp.route('/login', methods=['GET'])
def login():
    return render_template('/auth/login.html')


# DASHBOARD
@views_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('/dashboard/dashboard.html')


# User's Baits

@views_bp.route("/triggers", methods=['GET'])
def user_triggers():
    return render_template('/triggers/triggers.html')

# Alert Analytics Page
@views_bp.route("/analytics", methods=['GET'])
def alert_history():
    return render_template('history/analytics.html')

# About Page
@views_bp.route("/about", methods=['GET'])
def about():
    return render_template('/about/about.html')


# Downloads
@views_bp.route('/downloads/<filename>')
@jwt_required()  # only logged-in users can download bait
def download_bait(filename):

    @after_this_request
    def delete_file(response):
        try:
            os.unlink(os.path.join('static/downloads', filename))
            #print(f"[+] Cleaned Up {filename}")
        
        except Exception as e:
            #print(f'[+] Cleanup Failed {e}')
            pass
        
        return response
    
    return send_from_directory('static/downloads', filename, as_attachment=True)