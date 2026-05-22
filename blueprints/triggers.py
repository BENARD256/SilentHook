from models import db, Triggers, Baits, Users, Alerts, Watcher_events
from schemas import Triggerschema, ValidationError
from utils import api_response

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid # For Generating Unique Token IDs
import hashlib #

import os
from flask import current_app # accessing BASE CALLBACK_URL


# IMPORTING BAIT GENERATION MODULES

from services.msoffice import msoffice_bait # Generates office baits
from services.qrcode import qr_bait         # GenerateS Qr Code bait

"""
User Provides
    - Callback Email. If not We fetch Users.email then use it as Callback
    - Reminder

Possible Routes

POST /triggers/ - Create a new trigger
GET /triggers/ - Get all triggers for a particual user (using user_id as query param) # a reverse relation to fetch all triggers for a user
GET /triggers/<int:trigger_id> - Get a specific trigger by ID

# TRIGGERS
POST   /triggers/create/<bait_id>  attach trigger to a bait
GET    /triggers                   list all triggers for logged-in user
GET    /triggers/<trigger_id>      get a specific trigger
DELETE /triggers/<trigger_id>      delete a trigger

"""

# Blueprint for Trigger Routes
triggers_bp = Blueprint('triggers', __name__, url_prefix='/api/v1/triggers')

# Trigger Schema Init
trigger_schema = Triggerschema()


def generate_token(): # Generates a Longer Token
    token = str(uuid.uuid4())
    return hashlib.sha256(token.encode()).hexdigest()[:16]  # 16 Len HEX


# Function to Generate the Bait File. After Storing in the Db pull baits.bait_path
def generate_bait_file(token=None, bait_abbrv=None, template_path=None, center_image=None): 

    # Base Callback_url
    callback_url = current_app.config['CALLBACK_URL'] # Accessing url from config.py

    print( "TOKEN:", token, "BAIT_ABBREV: ", bait_abbrv, "TEMPLATE_PATH: ", template_path, "URL: ", callback_url,)

    # Constructing a Callback URL for all baits Via GET method
    # pdf, xlsx, docx, pptx, qr, domain
    callback_url_get = f"{callback_url}/token/{token}/callback" # Baseurl + "/token/ <TOKEN_ID> /callback"

    print("FINAL URL FOR GET BAITS: ", callback_url_get)
    # Comming up with an msoffice Bait

    office_baits = {
        'docx':       msoffice_bait,
        'xlsx':       msoffice_bait,
        'pptx':       msoffice_bait,
        'pdf':        None,
        'fim':        None,
        'mysql_dump': None
    }
    # MS OFFICE
    if bait_abbrv.lower() in office_baits:
        return office_baits[bait_abbrv.lower()](CALLBACK_URL=callback_url_get, TEMPLATE=template_path, TOKEN=token) # Returns static/downloads/7035ae6f-7b19-4f94-a1c3-bb7f3ff51973.xlsx


    # QR CODE
    if bait_abbrv.lower() == 'qr':
        return qr_bait(data=callback_url_get, logo_path=center_image, token=token)  # Returns /static/download/<token>.png (ONLY FILENAME)
 
    # DOMAIN
    if bait_abbrv.lower() == "domain":
        DOMAIN_LURES = [
            "/payroll/q2-review",
            "/hr/portal/login",
            "/it/vpn-access",
            "/finance/budget-approval",
        ]
        return [f"{callback_url}{path}?ref={token}" for path in DOMAIN_LURES]
    
    # Handles Untacked baits
    else:
        return "NOTHING BAIT MATCHED"


@triggers_bp.route("/create/<int:bait_id>", methods=['POST'])
@jwt_required()
def create_trigger(bait_id=None):
    
    bait_exists = Baits.query.get(bait_id)
    
    if not bait_exists:
        return api_response(
            message="Bait Not Valid",
            status="Error",
            code=404
        )

    # Detect QR with Image
    if request.content_type and 'multipart/form-data' in request.content_type:
        trigger_data = {'reminder': request.form.get('reminder'),  'callback_email': request.form.get('callback_email')}
    else:    
        trigger_data = request.json
     
    # Sanization & JSON Deserialization.
    try:
        trigger_data = trigger_schema.load(trigger_data, partial=True)  # Validation & Deserialize  of email, reminder to Dict not Database object 
        
    except ValidationError as err:
        return api_response(
            message="Validation Error",
            status="error",
            code=400,
            data={"errors": err.messages}
        )
    except Exception as err:
        return api_response(
            message="Internal Server Error",
            status="error",
            code=500,
            data={"error": str(err)}
        )
    
    # Fething user_id from JWT
    user_id = get_jwt_identity()
    
    # Verifying if callback email is given
    if not trigger_data.callback_email:
        trigger_data.callback_email = Users.query.get(user_id).email

    # Constructing trigger table data
    
    # Reminder & Email are Configured ealier
    trigger_data.token = generate_token()
    trigger_data.user_id = user_id
    trigger_data.bait_id = bait_id
    
    db.session.add(trigger_data) # Unpacking the Dict as Trigger DB Object before adding to db
    db.session.commit()
    db.session.refresh(trigger_data) # Refreshing Null Fields 
    

    # QRCODE BAIT IMAGE FILE
    center_image_path = None # Incase not  a QRBait
    if bait_exists.abbrev == 'QR' and 'qr_image' in request.files:
        file = request.files['qr_image']
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext in ['png', 'jpg', 'jpeg']:
            center_image_path = f'static/tmp/{trigger_data.token}_center.{ext}'
            file.save(center_image_path)

    
    # Bait Generation

    # bait_gen_data = Triggers.query.filter_by(token=trigger_data.token).first() # Filtering by the newly generated Token ID trigger_data.token

    # bait_type = bait_gen_data.bait.abbrev if bait_gen_data.bait.abbrev else "UNKNOWN"

    # print("Bait Type: ", bait_type)

    # msoffice_bait(CALLBACK_URL, TEMPLATE, TOKEN)


    # PULLING BAIT GENERATION DATA FROM bait_exists DB obj variable

    bait_abbrv = bait_exists.abbrev
    template_path  = bait_exists.bait_path
    
    bait_output = generate_bait_file(token=trigger_data.token, bait_abbrv=bait_abbrv, template_path=template_path, center_image=center_image_path) # Returns BAIT FILE

    print("Bait Output: is: ", bait_output)

    return api_response(
        data={"trigger": trigger_schema.dump(trigger_data), "filename":bait_output}, # Verify from front it its not accessed directly as filename
        message="Trigger created successfully",
        code=201
    )


# Retrieving Triggers for a specific User
@triggers_bp.route("/", methods=['GET'])
@triggers_bp.route("/<int:id>", methods=['GET']) # Watchout for this 
@jwt_required()
def get_triggers(id=None):
    user_id = get_jwt_identity() #
    print("TYPE OF JWT TRIGGERS: ", user_id, type(user_id))

    if id:
        # Single Trigger Filtered by id(table ID)
        user_trigger = Triggers.query.filter_by(id=id, user_id=user_id).first()

        if not user_trigger:
            return api_response(
                message = "Triggers Not Found",
                status = 'error',
                code = 404
            )
        
        return api_response(
            data={"trigger": trigger_schema.dump(user_trigger)},
            code=200
        )

    # Multiple Triggers as per the user id
    user_triggers = Triggers.query.filter_by(user_id=user_id).all() # Return all triggers that match the user id
    

    if not user_triggers:
        return api_response(
            message = "Triggers Not Found",
            status = 'error',
            code = 404
        )

    return api_response(
        data = trigger_schema.dump(user_triggers, many=True),
        message = "Triggers retrieved Successfully",
        code = 200
    )

# Method Not Yet Reliable

# understand what data we should return if baits are requested
@triggers_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_trigger(id=None): # user deleting a bait has to be the owner
    user_id = get_jwt_identity()

    if not id:
        return api_response(
            message = "Trigger ID required !",
            code    = 400
        )
    
    trigger = Triggers.query.filter_by(id=id, user_id=user_id).first()

    if not trigger:
        return api_response(
            message = "Trigger Not Found!",
            code    = 404
        )
    # Delete child alerts first before deleting the trigger. (Foreign Key relationship)
    Alerts.query.filter_by(token=trigger.token).delete()

    # Incase Bait Was FIM
    Watcher_events.query.filter_by(token=trigger.token).delete()  # (Clearing FK Relationships)

    # Future Tabes MySql 
    #MysqlEvents.query.filter_by(token=trigger.token).delete()

    db.session.delete(trigger)
    db.session.commit()
    # db.session.refresh(trigger) # IT errors during bait deletion

    return api_response(
        message = "Trigger Deleted Successfully",
        code    = 200
    )