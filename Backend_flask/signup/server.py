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

#--------------COMPANY----------------
# Sign Up for Company - Initial step for collecting data and sending verification code
@app.route('/company/signup', methods=['POST'])
def signup_club():
    data = request.json
    company_name = data.get('company_name')
    email = data.get('email')
    password = data.get('password')
    Industry = data.get('Industry')

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
    session['temp_signup_data_company'] = {
        'company_name': company_name,
        'Industry': Industry,
        'email': email,
        'password': password
    }

    return jsonify({"message": "Verification code sent to email"}), 200

# Verify Email and Complete Sign Up club
@app.route('/company/verify_email', methods=['POST'])
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
    temp_data = session.get('temp_signup_data_company')
    if not temp_data or temp_data['email'] != email:
        return jsonify({"error": "Sign-up session not found or email mismatch"}), 400

    # Save club details to the RDS database upon successful verification
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO CLUB_DETAILS (company_name, Industry, email, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            temp_data['company_name'],
            temp_data['Industry'],
            temp_data['email'],
            temp_data['password']
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    # Clear the temporary data
    del session['temp_signup_data_company']

    return jsonify({"message": "Company registered successfully"}), 201



#-------------CLUB-----------------
# Sign Up for Club - Initial step for collecting data and sending verification code
@app.route('/club/signup', methods=['POST'])
def signup_club():
    data = request.json
    club_name = data.get('club_name')
    email = data.get('email')
    password = data.get('password')
    college = data.get('college')

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
    session['temp_signup_data_club'] = {
        'club_name': club_name,
        'email': email,
        'password': password,
        'college': college
    }

    return jsonify({"message": "Verification code sent to email"}), 200

# Verify Email and Complete Sign Up club
@app.route('/club/verify_email', methods=['POST'])
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
    temp_data = session.get('temp_signup_data_club')
    if not temp_data or temp_data['email'] != email:
        return jsonify({"error": "Sign-up session not found or email mismatch"}), 400

    # Save club details to the RDS database upon successful verification
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO CLUB_DETAILS (club_name, email, password, college)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            temp_data['club_name'],
            temp_data['email'],
            temp_data['password'],
            temp_data['college']
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    # Clear the temporary data
    del session['temp_signup_data_club']

    return jsonify({"message": "Club registered successfully"}), 201

#------------------EVENTS---------------
# Get all the events for showcasing
@app.route("/get_events", METHODS = ["GET"])
def get_events():
    query = '''
        SELECT EVENT_NAME,CLUB_NAME,EVENT_DATE,LOCATION,AMOUNT,EVENT_DETAILS, FROM EVENT_DETAILS)
    '''
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query)
    query_output = cursor.fetchall()
    cursor.close()
    conn.close()
    response = {"data":
                    {
                        {
                            "EVENT_NAME":i[0],
                            "CLUB_NAME":i[1],
                            "EVENT_DATE":i[2],
                            "LOCATION":i[3],
                            "AMOUNT":i[4],
                            "EVENT_DETAILS":i[5]
                        } for i in query_output
                    }
                }
    return jsonify(response), 201

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
