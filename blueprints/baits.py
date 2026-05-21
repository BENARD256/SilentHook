from models import db, Baits
from schemas import Baitsschema, ValidationError
from utils import api_response
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

# Get all baits
# Get a specific bait by ID / Abbrv

"""
READ
/baits [GET] - Get all baits
/baits/<int:bait_id> [GET] - Get a specific bait by ID
/baits/?abbrev=abbrv [GET] - Get baits by abbreviation


ADMIN ONLY
/baits/ [POST] - Create a new bait
/baits/<int:bait_id> [PUT] - Update a bait by ID
/baits/<int:bait_id> [DELETE] - Delete a bait by ID

"""
# Besure Bait path isnt loaded in responses


# Blueprint for Baits Routes
baits_bp = Blueprint('baits', __name__, url_prefix='/api/v1/baits')


#baits Schema Initialization
bait_schema = Baitsschema()


@baits_bp.route("/", methods=['GET'])
@baits_bp.route('/<int:bait_id>', methods=['GET']) # Filter by ID
@baits_bp.route('/<string:abbrev>',methods=['GET']) # Filter by Abbreviation
@jwt_required()
def get_baits(bait_id=None, abbrev=None):
    if bait_id:
        bait = Baits.query.get(bait_id)
        if not bait:
            return api_response(message="Bait not found", status="error", code=404)
        print("BaitPath: ", )    
        return api_response(data=bait_schema.dump(bait), message="Bait retrieved successfully", code=200)
    
    if abbrev:
        bait = Baits.query.filter_by(abbrev=abbrev.upper()).first()
    
        if not bait:
            return api_response(message="Bait not found", status="error", code=404)
    
        return api_response(data=bait_schema.dump(bait), message="Bait retrieved successfully", code=200)
    

    baits = Baits.query.all()
    if not baits:
        return api_response(message="No baits found", status="error", code=404)
    
    return api_response(data=bait_schema.dump(baits, many=True), message="Baits retrieved successfully", code=200)


# Admin Only Routes

@baits_bp.route("/", methods=['POST'])
def create_bait():
    pass

@baits_bp.route("/<int:bait_id>", methods=['PUT'])
def update_bait(bait_id):
    pass

@baits_bp.route("/<int:bait_id>", methods=['DELETE'])
def delete_bait(bait_id):
    pass
