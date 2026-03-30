from flask import jsonify

# Standardises API Responses with consisten data structure

def api_response(data=None, message=None, status='success', code=200):

    payload = {'status': status}
    
    if message:
        payload['message'] = message
    if data:
        payload['data'] = data

    return jsonify(payload), code
