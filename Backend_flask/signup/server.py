from flask import Flask, request, jsonify, session
from flask_cognito import CognitoAuth
import mysql.connector
from werkzeug.security import generate_password_hash
import boto3

app = Flask(__name__)
app.secret_key = '123'

# Cognito Configuration
app.config['COGNITO_REGION'] = 'ap-south-1'  # Change to your AWS region
app.config['COGNITO_USERPOOL_ID'] = 'ap-south-1_TimL919pQ'
app.config['COGNITO_CLIENT_ID'] = '4ccp0ohq6uqv24sb4r74cj9abs'
# app.config['COGNITO_CLIENT_SECRET'] = 'your_client_secret'
# app.config['COGNITO_REDIRECT_URL'] = 'https://yourapp.com/callback'

cognito = CognitoAuth(app)

# Database Configuration (AWS RDS)
db_config = {
    'host': 'aws-database-2.cbg00emmolxk.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'iheqoEEP7673!',
    'database': 'AWS',
    'ssl_disabled': True
}

# AWS Cognito client setup
cognito_client = boto3.client('cognito-idp', region_name=app.config['COGNITO_REGION'])

# Sign Up for Club - Initial step for collecting data and sending verification code
@app.route('/signup/club', methods=['POST'])
def signup_club():
    data = request.json
    club_name = data.get('club_name')
    email = data.get('email')
    password = data.get('password')
    contact_number = data.get('contact_number')

    # Hash the password
    password_hash = password

    # Register user in Cognito and send a verification code to the email
    try:
        cognito_client.sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
            ]
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Store the temporary club data for later use upon verification
    session['temp_signup_data'] = {
        'club_name': club_name,
        'email': email,
        'password_hash': password_hash,
        'contact_number': contact_number
    }

    return jsonify({"message": "Verification code sent to email"}), 200

# Verify Email and Complete Sign Up
@app.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    # Verify the code with Cognito
    try:
        cognito_client.confirm_sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            Username=email,
            ConfirmationCode=code
        )
    except Exception as e:
        return jsonify({"error": "Invalid verification code or email"}), 400

    # Retrieve temporary signup data
    temp_data = session.get('temp_signup_data')
    if not temp_data or temp_data['email'] != email:
        return jsonify({"error": "Sign-up session not found or email mismatch"}), 400

    # Save club details to the RDS database upon successful verification
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO CLUB_DETAILS (club_name, email, password_hash, contact_number)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            temp_data['club_name'],
            temp_data['email'],
            temp_data['password_hash'],
            temp_data['contact_number']
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    # Clear the temporary data
    del session['temp_signup_data']

    return jsonify({"message": "Club registered successfully"}), 201

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
