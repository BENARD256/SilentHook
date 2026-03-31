from models import db, Triggers, Baits, Users
from schemas import Triggerschema, ValidationError
from utils import api_response

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid # For Generating Unique Token IDs

"""
User Provides
    - Callback Email. If not We fetch Users.email then use it as Callback
    - Reminder

Possible Routes

POST /triggers/ - Create a new trigger
GET /triggers/ - Get all triggers for a particual user (using user_id as query param) # a reverse relation to fetch all triggers for a user
GET /triggers/<int:trigger_id> - Get a specific trigger by ID

# TRIGGERS
POST   /triggers/create/<bait_id> → attach trigger to a bait
GET    /triggers                  → list all triggers for logged-in user
GET    /triggers/<trigger_id>     → get a specific trigger
DELETE /triggers/<trigger_id>     → delete a trigger

"""

# Blueprint for Trigger Routes
triggers_bp = Blueprint('triggers', __name__, url_prefix='/triggers')

# Trigger Schema Init
trigger_schema = Triggerschema()


def generate_token():
    return str(uuid.uuid4())

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

    # Reminder & Email are Configured ealier
    trigger_data.token_id = generate_token()
    trigger_data.user_id = user_id
    trigger_data.bait_id = bait_id
    
    db.session.add(trigger_data) # Unpacking the Dict as Trigger DB Object before adding to db
    db.session.commit()
    db.session.refresh(trigger_data) # Refreshing Null Fields 
    
    return api_response(
        data={"trigger": trigger_schema.dump(trigger_data)},
        message="Trigger created successfully",
        code=201
    )


@triggers_bp.route("/", methods=['POST'])
#@jwt_required() # Require JWT
def generate_trigger():
    token_id = generate_token()
    jwt_token = None #create_access_token(identity=token_id)
    return api_response(
        data={"token_id": token_id, "JWT": jwt_token},
        message="Token Generated Successfully",
        code=201
    )

    #current_user_id = get_jwt_identity() # Get the current user's ID from the JWT
    #return api_response(message=f"Trigger created successfully for user_id: {current_user_id}", code=201)


@triggers_bp.route("/me", methods=['GET'])
@jwt_required() # Require JWT
def me():
    user_id = get_jwt_identity()

    return api_response(
        data={"JWT": user_id, 'token_id': generate_token()},
        message="This is a protected route", 
        code=200
    )