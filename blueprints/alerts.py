from models import db, Alerts, Triggers, Watcher_events, Alert_history # Db Schemas
from schemas import Alertschema,Watcher_eventschema, ValidationError # Json Deserialization / Serialization
from utils import api_response

from flask import Blueprint, request, jsonify
from datetime import datetime
from services.mailing import mailer # Sending Email Alert to Users
from pathlib import Path

"""
Bait Callbacks Via GET

Docx    
xlsx
pdf
qrcode
domain
"""


callback_bp = Blueprint('callback', __name__, url_prefix='/token')

callback_domain_bp = Blueprint('callback_domain', __name__) # Specifically For domains

# Schema Objects
alert_schema = Alertschema()

watcher_schema = Watcher_eventschema()


def validate_token(token_id): # Before Triggering an Alert Verify if Token_id is Valid
    return Triggers.query.filter_by(token=token_id).first()


@callback_bp.route("<string:token_id>/callback", methods=['GET', 'HEAD', 'OPTIONS']) # xlsx, docx, pdf, qrcode
@callback_bp.route("<string:token_id>/callback/<path:extra>", methods=['GET', 'HEAD', 'OPTIONS']) # Clear PDF Bait Padding after /callback/
def handler_callback(token_id, extra=None):
     # Ignoring preflight and HEAD requests
    if request.method in ['OPTIONS', 'HEAD']:
        return '', 200
    
    trigger_token = validate_token(token_id)

    if not trigger_token:
        return api_response(message="Invalid token", status="error", code=404)
    
    #print("EMAIL AND REMINDER VERIFICATION", trigger_token.reminder, trigger_token.callback_email)
    


    # Bulding Alert
    source_ip = request.headers.get('X-Forwarded-For', request.remote_addr) # Source Ip
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

    # Alerts to Alerts_History
    history = Alert_history(
        token = trigger_token.token,
        bait_type = trigger_token.bait.abbrev,
        source_ip = source_ip,
        user_id = trigger_token.user_id
    )
    # Alert_History DB Save
    db.session.add(history)
    db.session.commit()

    # SENDING EMAIL ALERTS
    bait_type = trigger_token.bait.abbrev if trigger_token.bait else "UNKNOWN"

    alert_dictionary = alert_schema.dump(alert) # Dictionary of all details in the Alert
    #print(alert_dictionary)

    print("EMAILING..")
    mailer(dst_mail=trigger_token.callback_email, bait_type=bait_type, reminder=trigger_token.reminder, alert_dict=alert_dictionary)
    print("SENT")

    return api_response(
        data=alert_schema.dump(alert),
        message="Valid" 
    )


# Domain Callbacks
@callback_domain_bp.route("/payroll/q2-review", methods=['GET']) # https://dbbd.com/payroll/q2-review?ref={short_token(token)}
@callback_domain_bp.route("/hr/portal/login", methods=['GET'])
@callback_domain_bp.route("/it/vpn-access", methods=['GET'])
@callback_domain_bp.route("/finance/budget-approval", methods=['GET'])
def domain_callback():
    token_id = request.args.get('ref') # Pull token Given as Reference

    trigger_token = validate_token(token_id=token_id)

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

    # Alerts to Alerts_History
    history = Alert_history(
        token = trigger_token.token,
        bait_type = trigger_token.bait.abbrev,
        source_ip = source_ip,
        user_id = trigger_token.user_id
    )
    # Alert_History DB Save
    db.session.add(history)
    db.session.commit()

    # SENDING EMAIL ALERTS
    bait_type = trigger_token.bait.abbrev if trigger_token.bait else "UNKNOWN"

    alert_dictionary = alert_schema.dump(alert) # Dictionary of all details in the Alert
    #print(alert_dictionary)

    print("EMAILING..")
    mailer(dst_mail=trigger_token.callback_email, bait_type=bait_type, reminder=trigger_token.reminder, alert_dict=alert_dictionary)
    print("SENT")

    return api_response(
        data=alert_schema.dump(alert),
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
    # Windows background system processes
    'svchost.exe',
    'searchindexer.exe',        # Windows Search indexing
    'searchprotocolhost.exe',   # Windows Search
    'searchfilterhost.exe',     # Windows Search
    'trustedinstaller.exe',     # Windows Update
    'tiworker.exe',             # Windows Update
    'wuauclt.exe',              # Windows Update
    'spoolsv.exe',              # Print spooler
    'taskhostw.exe',            # Task scheduler
    'wermgr.exe',               # Windows Error Reporting
    'backgroundtaskhost.exe',   # Background tasks
    'dllhost.exe',              # COM surrogate

    # Cloud sync auto-scan files silently
    'onedrivesetup.exe',        # OneDrive setup scan
    'googledrivesync.exe',      # Google Drive sync
    'dropbox.exe',              # Dropbox sync

    # Antivirus real-time protection  auto-scan only
    'msmpeng.exe',              # Windows Defender
    'nissrv.exe',               # Windows Defender Network
    'mpcmdrun.exe',             # Windows Defender CLI
    'smdrtp.exe',               # Smadav RTP
    'avguard.exe',              # Avira
    'ekrn.exe',                 # ESET
    'mbamservice.exe',          # Malwarebytes service
    'mcshield.exe',             # McAfee shield
    'bdagent.exe',              # Bitdefender agent
    'avgsvc.exe',               # AVG service
    'avastsvc.exe',             # Avast service
    'savservice.exe',           # Sophos service
    'cmdagent.exe',             # Comodo agent
    'tmbmsrv.exe',              # Trend Micro service
}


NOISE_PATHS = {
    'desktop.ini',
    'desktop.INI',
    'DESKTOP.INI',
    'thumbs.db',
    '.ds_store',
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
        print("error:", err.messages) # DEBUGGING LINE
        return {"errors": err.messages}, 400 # Bad Request
    except Exception as err:
        return {"error": str(err)}, 500 # Internal Server Error
    
    # Noisy Access Type
    if watcher_event.access in SKIP:
        return '', 204
    
    # Noisy Paths desktop.ini 
    filename = Path(watcher_event.path).name.lower()
    if filename in NOISE_PATHS:
        return '', 204
    
    # Replacing Mask with Label
    watcher_event.access = ACCESS_MAP.get(watcher_event.access, watcher_event.access) # Replacing The Mask

    # Deduplication of Events. prevents spam alerts for a single Event
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

    # Alerts to Alerts_History
    history = Alert_history(
        token = trigger_token.token,
        bait_type = trigger_token.bait.abbrev,
        source_ip = request.remote_addr,
        user_id = trigger_token.user_id
    )
    # Alert_History DB Save
    db.session.add(history)
    db.session.commit()

    # SENDING EMAIL ALERTS

    to_email = watcher_event.trigger_info.callback_email
    bait_type = trigger_token.bait.abbrev if trigger_token.bait else "UNKNOWN"
    reminder = watcher_event.trigger_info.reminder
    alert_dictionary = watcher_schema.dump(watcher_event) # Dictionary of all details in the Alert
    #print("ALERT DICTIONARY DUMPL ", alert_dictionary)
    
    print("EMAILING..")
    mailer(dst_mail=trigger_token.callback_email, bait_type=bait_type, reminder=trigger_token.reminder, alert_dict=alert_dictionary)
    print("SENT.")

    
    # DEBUG LINES
    """
    print("\n")
    print("#"*50)
    for key, value in watcher_schema.dump(watcher_event).items():
        print(key, ":", value)
    print("#"*50)

    print("\n")

    """
    return api_response(
        data=watcher_schema.dump(watcher_event),
        message="Valid"
    )