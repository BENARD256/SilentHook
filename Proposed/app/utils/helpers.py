from flask import jsonify

## Helper functions for consistent API responses and error handling
def success(data, status=200):
    return jsonify({"success": True, "data": data}), status

def error(message, status=400):
    return jsonify({"success": False, "error": message}), status

## ACcesing a resource that does not exist
def not_found(message="Resource not found"):
    return error(message, status=404)



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
    except Exception as e:
        #### this is not configured yet  from line 30 -32
        ## failed due to wrong credentials, network issues, or DB server down
        #default_message = "Database Connection Failed. Please check your database configuration and ensure the database server is running."     

        return error(f"Database Connection Failed: {e}", status=500)
    else:
        return success("Database Connection Successful", status=200)