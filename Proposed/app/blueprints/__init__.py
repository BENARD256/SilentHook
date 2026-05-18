from .auth import auth_bp, auth_api_bp
from .baits import baits_bp
from .triggers import triggers_bp
from .alerts import callback_bp
from .views import views_bp, auth_page_bp

ALL_BLUEPRINTS = [
    auth_bp,
    auth_api_bp,
    baits_bp,
    triggers_bp,
    callback_bp,
    views_bp,
    auth_page_bp,
]

__all__ = [
    "auth_bp", "auth_api_bp",
    "baits_bp", "triggers_bp",
    "callback_bp", "views_bp",
    "auth_page_bp", "ALL_BLUEPRINTS"
]