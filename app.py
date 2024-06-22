import random
from flask import Flask, request, jsonify
from twilio.rest import Client
from pydantic import BaseModel, ValidationError
from typing import Optional
from waitress import serve

app = Flask(__name__)

TWILIO_ACCOUNT_SID = 'AC267eb2d53a1a6409a2f8d6b2e324e4fd'
TWILIO_AUTH_TOKEN = 'c5f303934444ec9179fbff1acdbab10c'
TWILIO_SERVICES_ID = 'VA9640251ab8c925c8b896af7099ff2d65'





client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Define Pydantic models for request validation
class SendOtpRequest(BaseModel):
    phone_number: str

class VerifyOtpRequest(BaseModel):
    phone_number: str
    otp_code: str

@app.route('/send_otp', methods=['POST'])
def send_otp():
    try:
        # Parse and validate the request data
        data = request.json
        send_otp_request = SendOtpRequest(**data)
        
        # Send the OTP
        verification = client.verify.v2.services(TWILIO_SERVICES_ID).verifications.create(
            to=send_otp_request.phone_number, 
            channel="sms"
        )
        
        # Return the status as a JSON response
        return jsonify({"status": verification.status}), 200
    
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verify_otp", methods=['POST'])
def verify_otp():
    try:
        # Parse and validate the request data
        data = request.json
        verify_otp_request = VerifyOtpRequest(**data)
        
        # Verify the OTP
        verification_check = client.verify.v2.services(TWILIO_SERVICES_ID).verification_checks.create(
            to=verify_otp_request.phone_number, 
            code=verify_otp_request.otp_code
        )
        
        # Return the status as a JSON response
        return jsonify({"status": verification_check.status}), 200
    
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    
    #app.run(debug=True, use_reloader=True, reloader_type='stat')
    serve(app, host='0.0.0.0', port=8000)
    

