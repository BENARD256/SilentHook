from .auth import auth_bp, auth_api_bp # Auth Blueprint for APIs & Page Routes
from .baits import baits_bp # Baits Blueprint
from .triggers import triggers_bp # Triggers Blueprint
from .alerts import callback_bp # Alerts (callback) Blueprint
from .import views # HTML Page Rendering
from .extensions import db, jwt, cache # Importing Extensions for DB, JWT, and Caching
from .config import Config, DevelopmentConfig, ProductionConfig # Importing Configurations
from flask import Flask, request, render_template, jsonify

