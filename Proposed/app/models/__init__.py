from .user import Users 
from .bait import Baits 
from .trigger import Triggers 
from .alert import Alerts 
from .watcher_events import Watcher_events
from .mysql_events import Mysql_events 
from .alert_history import Alert_history 

# This __init__.py file is used to import all the models into a single namespace, making it easier to access them throughout the application without needing to import each model individually in different files. By importing the models here, you can simply import the models package and have access to all the defined models in your application.
__all__ = [
    "Users",
    "Baits",
    "Triggers",
    "Alerts",
    "Watcher_events",
    "Mysql_events",
    "Alert_history"
]
