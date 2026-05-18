# SHARED HELPERS
# api_response() is the standard response format for all routes.
# Do not return raw jsonify() in blueprints — use this instead.


from curses import error

from django.db import connection
from flask import jsonify

## Helper functions for consistent API responses and error handling
def api_response(data=None, message=None, code =None, error=None, status=200):
    
    if code is not None:
        response = { "code": code }
    else:
        response = { }


    if error is not None:
        response["success"] = False
        response["error"] = error

        if status == 200:
            status = 400

    else:
        response["success"] = True
    
    if message:
            response["message"] = message

    if data is not None:
        response["data"] = data
    
    return jsonify(response), status

    
## ACcesing a resource that does not exist
def not_found(message="Resource not found"):
    return api_response(success=False, error=message, status=404)



## Helper function to format validation errors from Marshmallow
def format_validation_errors(errors):
    formatted_errors = []
    for field, messages in errors.items():
        for message in messages:
            formatted_errors.append(f"{field}: {message}")
    return formatted_errors 


## database connection helper function and error handling can be added here as needed, but for now we will keep it simple and handle DB connection errors in the app initialization phase.
def test_db_connection(db):
    try:
        db.engine.connect()
        connection.close()
    except Exception as e:
        #### this is not configured yet  from line 30 -32
        ## failed due to wrong credentials, network issues, or DB server down
        #default_message = "Database Connection Failed. Please check your database configuration and ensure the database server is running."     

        return api_response(success=False, error=f"Database Connection Failed: {e}", status=500)
    else:
        return api_response(success=True, data="Database Connection Successful", status=200)