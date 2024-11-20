from flask import Flask, request, jsonify, session
from flask_cognito import CognitoAuth
import mysql.connector
from werkzeug.security import generate_password_hash
import boto3
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '123'
CORS(app)

# Cognito Configuration
app.config['COGNITO_REGION'] = 'ap-south-1'  # Change to your AWS region
app.config['COGNITO_USERPOOL_ID'] = 'ap-south-1_TimL919pQ'
app.config['COGNITO_CLIENT_ID'] = '4ccp0ohq6uqv24sb4r74cj9abs'

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

#--------------COMPANY SIGNUP----------------
# Sign Up for Company - Initial step for collecting data and sending verification code
@app.route('/company/signup', methods=['POST'])
def signup_conpany():
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
def comapany_verify_email():
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
            INSERT INTO COMPANY_DETAILS (company_name, Industry, email, password)
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



#-------------CLUB SIGNUP-----------------
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

#----------------LOGINS----------------
@app.route('/club/login', methods=['POST'])
def club_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to check if the club exists
        query = "SELECT club_id, email, password FROM CLUB_DETAILS WHERE email = %s"
        cursor.execute(query, (email,))
        club = cursor.fetchone()

        if not club:
            return jsonify({"error": "Invalid email or password"}), 401

        # Verify the password
        if not password == club["password"]:  # Replace with hashed password check
            return jsonify({"error": "Invalid email or password"}), 401

        # Set session or return a response
        session['club_id'] = club['club_id']

        return jsonify({
            "message": "Club login successful",
            "club_id": club['club_id']
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/company/login', methods=['POST'])
def company_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to check if the company exists
        query = "SELECT company_id, email, password FROM COMPANY_DETAILS WHERE email = %s"
        cursor.execute(query, (email,))
        company = cursor.fetchone()

        if not company:
            return jsonify({"error": "Invalid email or password"}), 401

        # Verify the password
        if not password == company["password"]:  # Replace with hashed password check
            return jsonify({"error": "Invalid email or password"}), 401

        # Set session or return a response
        session['company_id'] = company['company_id']

        return jsonify({
            "message": "Company login successful",
            "company_id": company['company_id']
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

#------------------EVENTS---------------
# Get all the events for showcasing
@app.route("/get_events", methods=["GET"])
def get_events():
    query = '''
        SELECT EVENT_NAME,CLUB_NAME,EVENT_DATE,LOCATION,AMOUNT,EVENT_DETAILS,EVENT_IMG FROM EVENT_DETAILS)
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
                            "EVENT_DETAILS":i[5],
                            "EVENT_IMG":i[6]
                        } for i in query_output
                    }
                }
    return jsonify(response), 201

@app.route('/confirm_sponsorship', methods=['POST'])
def confirm_sponsorship():
    data = request.json
    sponsor_id = data.get('sponsor_id')
    event_id = data.get('event_id')
    amount = data.get('amount')

    if not sponsor_id or not event_id or not amount:
        return jsonify({"error": "Sponsor ID, Event ID, and Amount are required"}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the event details
        fetch_event_query = "SELECT * FROM EVENT_DETAILS WHERE event_id = %s"
        cursor.execute(fetch_event_query, (event_id,))
        event = cursor.fetchone()

        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Remove the event from EVENT_DETAILS
        delete_event_query = "DELETE FROM EVENT_DETAILS WHERE event_id = %s"
        cursor.execute(delete_event_query, (event_id,))

        # Insert the sponsorship details into SPONSOR_CONFIRM
        insert_confirm_query = """
            INSERT INTO SPONSOR_CONFIRM (sponsor_id, event_id, amount, confirmation_date)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(insert_confirm_query, (sponsor_id, event_id, amount))

        # Commit the changes
        conn.commit()

        return jsonify({"message": "Sponsorship confirmed and event removed from EVENT_DETAILS"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.form
    event_name = data.get('event_name')
    club_id = data.get('club_id')
    event_date = data.get('event_date')
    location = data.get('location')
    amount = data.get('amount')
    event_details = data.get('event_details')

    # Get the event image from the request (binary data)
    event_image = request.files.get('event_image')

    # Ensure all required fields are provided
    if not event_name or not club_id or not event_date or not location or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    # Convert the event image to binary if it exists
    event_image_data = None
    if event_image:
        event_image_data = event_image.read()  # Read image as binary

    try:
        # Establish database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to insert event data
        query = """
            INSERT INTO EVENT_DETAILS 
            (event_name, club_id, event_date, location, amount, event_details, event_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            event_name,
            club_id,
            event_date,
            location,
            amount,
            event_details,
            event_image_data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Event added successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
