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
def signup_company():
    data = request.json
    company_name = data.get('company_name')
    email = data.get('email')
    password = data.get('password')
    industry = data.get('industry')

    try:
        # Save temporary data to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO TEMP_COMPANY_SIGNUP (email, company_name, password, industry)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            company_name = VALUES(company_name), password = VALUES(password), industry = VALUES(industry)
        """
        cursor.execute(query, (email, company_name, password, industry))
        conn.commit()
        cursor.close()
        conn.close()

        # Send verification code through Cognito
        cognito_client.sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            Username=email,
            Password=password,
            UserAttributes=[{'Name': 'email', 'Value': email}],
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Verification code sent to email"}), 200

# Verify Email and Complete Sign Up club
@app.route('/company/verify_email', methods=['POST'])
def verify_email_company():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    try:
        # Verify the code with Cognito
        cognito_client.confirm_sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            Username=email,
            ConfirmationCode=code
        )

        # Retrieve temporary signup data from the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM TEMP_COMPANY_SIGNUP WHERE email = %s"
        cursor.execute(query, (email,))
        temp_data = cursor.fetchone()

        if not temp_data:
            return jsonify({"error": "No signup data found for this email"}), 404

        # Save the verified data to COMPANY_DETAILS
        query = """
            INSERT INTO COMPANY_DETAILS (company_name, email, password, industry)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            temp_data['company_name'],
            temp_data['email'],
            temp_data['password'],
            temp_data['industry']
        ))
        conn.commit()

        # Clean up temporary data
        cursor.execute("DELETE FROM TEMP_COMPANY_SIGNUP WHERE email = %s", (email,))
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

    try:
        # Save temporary data to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO TEMP_SIGNUP (email, club_name, password, college)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            club_name = VALUES(club_name), password = VALUES(password), college = VALUES(college)
        """
        cursor.execute(query, (email, club_name, password, college))
        conn.commit()
        cursor.close()
        conn.close()

        # Send verification code through Cognito
        cognito_client.sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            Username=email,
            Password=password,
            UserAttributes=[{'Name': 'email', 'Value': email}],
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Verification code sent to email"}), 200


@app.route('/club/verify_email', methods=['POST'])
def verify_email():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    try:
        # Verify the code with Cognito
        cognito_client.confirm_sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            Username=email,
            ConfirmationCode=code
        )

        # Retrieve temporary signup data from the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM TEMP_SIGNUP WHERE email = %s"
        cursor.execute(query, (email,))
        temp_data = cursor.fetchone()

        if not temp_data:
            return jsonify({"error": "No signup data found for this email"}), 404

        # Save the verified data to CLUB_DETAILS
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

        # Clean up temporary data
        cursor.execute("DELETE FROM TEMP_SIGNUP WHERE email = %s", (email,))
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
import base64

@app.route("/get_events", methods=["GET"])
def get_events():
    query = '''
        SELECT event_name, club_name, event_date, location, amount, event_details, event_image, event_id FROM EVENT_DETAILS
    '''
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query)
    query_output = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert binary image data to base64 string
    response = {"data": [
        {
            "id":i[7],
            "title": i[0],
            "clubName": i[1],
            "date": i[2],
            "location": i[3],
            "sponsorshipNeeded": i[4],
            "description": i[5],
            "image": i[6] # encode image to base64
        } for i in query_output
    ]}
    return jsonify(response), 200

@app.route('/confirm_sponsorship', methods=['POST'])
def confirm_sponsorship():
    data = request.json

    # Extract data from the request
    sponsor_email = data.get('email')
    event_id = data.get('eventId')
    amount = data.get('amount')
    # message = data.get('message')

    if not sponsor_email or not event_id or not amount:
        return jsonify({"error": "Sponsor ID, Event ID, and Amount are required"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch event details
        fetch_event_query = """
            SELECT e.amount, e.club_id, c.email 
            FROM EVENT_DETAILS e
            JOIN CLUB_DETAILS c ON e.club_id = c.club_id
            WHERE e.event_id = %s
        """
        cursor.execute(fetch_event_query, (event_id,))
        event = cursor.fetchone()

        if not event:
            return jsonify({"error": "Event not found"}), 404

        remaining_amount, club_id, club_email = event

        if remaining_amount <= amount:
            # If the full amount is covered, delete the event
            delete_event_query = "DELETE FROM EVENT_DETAILS WHERE event_id = %s"
            cursor.execute(delete_event_query, (event_id,))
            status_message = "Full sponsorship received. Event removed from EVENT_DETAILS."
        else:
            # Update the remaining amount in EVENT_DETAILS
            update_event_query = """
                UPDATE EVENT_DETAILS 
                SET amount = amount - %s 
                WHERE event_id = %s
            """
            cursor.execute(update_event_query, (amount, event_id))
            status_message = "Partial sponsorship received. Remaining amount updated in EVENT_DETAILS."

        # Insert sponsorship confirmation into SPONSOR_CONFIRM
        insert_confirm_query = """
            INSERT INTO SPONSOR_CONFIRM (sponsor_id, event_id, amount, confirmation_date)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(insert_confirm_query, (sponsor_email, event_id, amount))

        # Send email to the club
        # send_email_to_club(club_email, sponsor_email, event_id, amount)

        # Commit the transaction
        conn.commit()

        return jsonify({"message": status_message}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json

    # Extract data from the request
    club_email = data.get('clubEmail')
    event_name = data.get('title')
    event_date = data.get('date')
    location = data.get('location')
    amount = data.get('sponsorshipNeeded')
    event_details = data.get('description')
    event_image = data.get('image')  # Assuming event_image is provided as a URL

    # Ensure all required fields are provided
    if not club_email or not event_name or not event_date or not location or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Establish database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch club_id from CLUB_DETAILS using clubEmail
        fetch_club_id_query = "SELECT club_id FROM CLUB_DETAILS WHERE email = %s"
        cursor.execute(fetch_club_id_query, (club_email,))
        club_id = cursor.fetchone()

        if not club_id:
            return jsonify({"error": "Club not found with the provided email"}), 404

        # Insert event into EVENT_DETAILS
        insert_event_query = """
            INSERT INTO EVENT_DETAILS 
            (event_name, club_id, event_date, location, amount, event_details, event_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_event_query, (
            event_name,
            club_id[0],  # Extracting club_id from the fetched result
            event_date,
            location,
            amount,
            event_details,
            event_image
        ))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        return jsonify({"message": "Event added successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if conn.is_connected():
            conn.close()

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
