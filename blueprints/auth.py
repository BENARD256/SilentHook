from models import db, Users # Database & User Model
from schemas import Userschema, ValidationError # Json Schema for User Model
from utils import api_response #Function for Standardizing API Responses


from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash, check_password_hash # For Password Hashing & Validation

# Blueprint for Authentication Page Routes & APIs


auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # Blueprint for Auth Page Routes
auth_api_bp = Blueprint('auth_api', __name__, url_prefix='/api/v1/auth') # api route for APIS

# Users Json Schema Instance
user_schema = Userschema()


@auth_api_bp.route("/users", methods=['GET'])
@auth_api_bp.route("/users/<int:user_id>", methods=['GET'])
def get_users(user_id=None):
    if not user_id: # Return All users
        users = Users.query.all() # Fetching all users from the database
    
        # Validating Empty User List
        if not users:
            return {'error':'User Not Found'}, 404 # User not found
    
        users = user_schema.dump(users, many=True) # Serializing the user data using the User Schema
    
        return users, 200
    
    # Returning a Specific User by ID

    user = Users.query.get(user_id) #get_or_404(user_id) # Fetching a specific user by ID and catches error

    if not user:
        return {'error':'User Not Found'}, 404 # User not found
        
    users = user_schema.dump(user)

    return users, 200


@auth_api_bp.route("/register", methods=['POST'])
def register_api():
    # Handling Registration 
    try:
        user = user_schema.load(request.json)  # Deserialization of incoming json data
    
    except ValidationError as err:
        return {"errors": err.messages}, 400 #  Bad Request status code
    
    except Exception as err:
        return {"error": str(err)}, 500 # Internal Server Error status code

    # Checking Data With Database User Records
    existing = Users.query.filter((Users.email == user.email) | (Users.username == user.username)).first()

    if existing:
        if existing.email == user.email:
            return {"error": "Email already exists"}, 400 # Bad Request
        
        if existing.username == user.username:
            return {"error": "Username already taken"}, 400 # Bad Request   
    

    user.password = generate_password_hash(user.password)
    db.session.add(user)
    db.session.commit()

    #return user_schema.dump(user), 201 # Created
    return api_response(
        data={"user": user_schema.dump(user)},
        message="Account created successfully",
        code=201
    )


@auth_api_bp.route("/login", methods=['POST'])
def login_api():
    user_logins = request.json
    try:
        user_logins = user_schema.load(user_logins, partial=True)  # Deserialization user logins
    
    except ValidationError as err:
        return {"errors": err.messages}, 400 # Bad Request
    except Exception as err:
        return {"error": str(err)}, 500 # Internal Server Error
    
    # Authenticating User Logins
    user = Users.query.filter_by(email=user_logins.email).first()

    if not user or not check_password_hash(user.password, user_logins.password):
        return {"error": "Invalid email or password"}, 401 # Unauthorized

    # JWT Token Generation
    jwt_token = create_access_token(identity=user.id)

    #return user_schema.dump(user), 200 # OK  
    return api_response(
        data={"user": user_schema.dump(user), "JWT": jwt_token},
        message="Logged in successfully",
        code=200
    )
    

@auth_api_bp.route("/logout", methods=['POST'])
def logout():
    # Logout Logic Token Invalidation, Session Clearing
    #return jsonify({"status": "success", "message": "Logged out successfully"}), 200 # OK
    return api_response(
        message="Logged out successfully",
        code=200
    )



@auth_api_bp.route("users/<int:user_id>", methods=['PUT'])
def update_user(user_id): # password reset, email update, username update
    pass

@auth_api_bp.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id): # User Deletion
    pass
