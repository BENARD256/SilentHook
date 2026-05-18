#from models import db, Triggers, Baits, Users
#from schemas import Triggerschema, ValidationError
#from utils import api_response

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid # For Generating Unique Token IDs

import os
from flask import current_app # accessing Callback UR
## updated imports
from app.extensions import db # Importing the database instance from extensions
from app.models import Triggers, Baits, Users # Importing the Triggers, B
from app.schemas import Triggerschema # Importing the Triggers schema
from app.utils.helpers import api_response # Importing the helper function for standardized API responses





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


def generate_token():
    return str(uuid.uuid4())



# Function to Generate the Bait File. After Storing in the Db pull baits.bait_path
def generate_bait_file(bait_id=None): # bait_id --> bait.bait_path . It will be called after validating the paths in create trigger

    # Callback_url
    callback_url = current_app.config['CALL_BACK_URL'] # Accessing from config.py

    bait_path = Baits.query.get(bait_id).bait_path # Bait path from baits table

    if os.path.exists(bait_path):
        pass
    else:
        pass
    
    print("Bait Id:", bait_id, "PATH: ", bait_path, "URL: ", callback_url)


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

    trigger_data = request.json
    
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
    
    generate_bait_file(bait_id=bait_id) # Bait Generation

    return api_response(
        data={"trigger": trigger_schema.dump(trigger_data)},
        message="Trigger created successfully",
        code=201
    )


# Retrieving Triggers for a specific User
@triggers_bp.route("/", methods=['GET'])
@triggers_bp.route("/<int:id>", methods=['GET']) # Watchout for this 
@jwt_required()
def get_triggers(id=None):
    user_id = get_jwt_identity() #
    #print("TYPE OF JWT TRIGGERS: ", user_id, type(user_id))

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
    
    db.session.delete(trigger)
    db.session.commit()
   #db.session.refresh()
    return api_response(
        message = "Trigger Deleted Successfully",
        code    = 200
    )