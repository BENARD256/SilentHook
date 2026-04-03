from models import db, Alerts, Triggers, Watcher_events # Db Schemas
from schemas import Alertschema,Watcher_eventschema, ValidationError # Json Deserialization / Serialization
from utils import api_response

from flask import Blueprint, request, jsonify
from datetime import datetime

"""
Bait Callbacks Via GET

Docx    
xlsx
pdf
qrcode
domain
"""


callback_bp = Blueprint('callback', __name__, url_prefix='/token')

# Schema Objects
alert_schema = Alertschema()

watcher_schema = Watcher_eventschema()


def validate_token(token_id): # Before Triggering an Alert Verify if Token_id is Valid
    return Triggers.query.filter_by(token=token_id).first()


@callback_bp.route("<string:token_id>/callback", methods=['GET']) # xlsx, docx, pdf, qrcode
def msoffice_callback(token_id):
    trigger_token = validate_token(token_id)

    if not trigger_token:
        return api_response(message="Invalid token", status="error", code=404)


    # Bulding Alert
    source_ip = request.remote_addr # Source IP
    user_agent = request.headers.get('User-Agent', "Unknow")

    alert = Alerts(
        token = trigger_token.token, # Triggers.id : pointing to the specific token
        source_ip = source_ip,
        user_agent = user_agent
    )
    
    # Alert to DB

    db.session.add(alert)
    db.session.commit()
    
    # Refreshing Db Session
    db.session.refresh(alert) # Making Sure it Returns updated Results

    return api_response(
        data=alert_schema.dump(alert),
        message="Valid"
    )


# Domain Callback
@callback_bp.route("<string:token_id>/payroll", methods=['GET'])
def domain_callback(token_id):
    trigger_token = validate_token(token_id=token_id)

    if not trigger_token:
        return api_response(message="Invalid token", status="error", code=404)

    return api_response(
        data=trigger_token.token,
        message="Valid"
    )

###################################################     FIM ENDPOINT    #############################################
seen = set()

ACCESS_MAP = {
    '0x1'     : 'ListDirectory / ReadData',
    '0x2'     : 'WriteData / AddFile',
    '0x4'     : 'AppendData / AddSubdir',
    '0x6'     : 'WriteData + AppendData',
    '0x8'     : 'ReadExtendedAttributes',
    '0x10'    : 'WriteExtendedAttributes',
    '0x20'    : 'Execute / Traverse',
    '0x40'    : 'DeleteChild',
    '0x80'    : 'ReadAttributes',
    '0x100'   : 'WriteAttributes',
    '0x10000' : 'Delete',
    '0x20000' : 'ReadControl',
    '0x40000' : 'ChangePermissions',
    '0x80000' : 'TakeOwnership',
    '0x120089': 'Read',
    '0x120116': 'Write',
    '0x1200a0': 'Execute',
    '0x1f01ff': 'FullControl',
}

SKIP       = {'0x80', '0x100', '0x20000'}

SUSPICIOUS = ['powershell', 'cmd', 'python', 'nc.exe', 'meterpreter',
              'psexec', 'wscript', 'cscript', 'rundll32', 'mshta']

NOISE_PROCESSES = {
    'msmpeng.exe',
    'svchost.exe',
    'searchindexer.exe',
    'searchprotocolhost.exe',
    'trustedinstaller.exe',
    'tiworker.exe',
    'wuauclt.exe',
    'spoolsv.exe',
}

#Watcher callback
@callback_bp.route("<string:token>/fim", methods=['POST'])
def fim_callback(token):
    
    trigger_token = validate_token(token_id=token)
    if not trigger_token:
        return api_response(message="Invalid token", status="error", code=404)        

    # Fetch Request
    watcher_event = request.json

    # Sanitization & Validation
    try:
        watcher_event = watcher_schema.load(watcher_event, partial=True)
    except ValidationError as err:
        return {"errors": err.messages}, 400 # Bad Request
    except Exception as err:
        return {"error": str(err)}, 500 # Internal Server Error
    
    # Noisy Access Type
    if watcher_event.access in SKIP:
        return '', 204
    
    # Replacing Mask with Label
    watcher_event.access = ACCESS_MAP.get(watcher_event.access, watcher_event.access) # Replacing The Mask

    # Deduplication of Events
    event_exists = Watcher_events.query.filter_by(
        user = watcher_event.user,
        path = watcher_event.path,
        access = watcher_event.access,
        event_time = watcher_event.event_time
    ).first()

    if event_exists:
        return '', 204
    

    #Noisy Process
    process_name = watcher_event.process.split('\\')[-1].lower() # Trim the path, preserve only the executable

    if process_name in NOISE_PROCESSES:
        return "", 204
    
    
    # filling other fields
    watcher_event.token = trigger_token.token # using a token from the database
    watcher_event.source_ip = request.remote_addr

    # Events to DB
    db.session.add(watcher_event)
    db.session.commit()
    db.session.refresh(watcher_event)

    return api_response(
        data=watcher_schema.dump(watcher_event),
        message="Valid"
    )