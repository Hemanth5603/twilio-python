import random
from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

TWILIO_ACCOUNT_SID = 'AC267eb2d53a1a6409a2f8d6b2e324e4fd'
TWILIO_AUTH_TOKEN = '4ccc5f9026da475158c111f30c4e91c0'
TWILIO_PHONE_NUMBER = '+15642167867'
TWILIO_SERVICES_ID='VA9640251ab8c925c8b896af7099ff2d65'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
otp_storage = {}

def generate_otp():
    return str(random.randint(100000,9999999))




@app.route('/send_otp', methods=['POST'])
def send_otp():
    verification = client.verify.v2.services(
        TWILIO_SERVICES_ID
    ).verifications.create(to="+917997435603", channel="sms")
    print(verification.status)
    





@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)

