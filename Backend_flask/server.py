from flask import Flask, request, jsonify
import mysql.connector
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Amazon RDS MySQL connection configuration
db_config = {
    'user': 'admin',
    'password': 'iheqoEEP7673!',
    'host': 'aws-database-2.cbg00emmolxk.ap-south-1.rds.amazonaws.com',
    'database': 'AWS',
    'ssl_disabled':True
}

# Amazon Cognito configuration
cognito_client = boto3.client('cognito-idp', region_name='ap-south-1')
user_pool_id = 'ap-south-1_TimL919pQ'
client_id = '4ccp0ohq6uqv24sb4r74cj9abs'

# Function to connect to the MySQL database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Club Signup
# @app.route('/club/signup', methods=['POST'])
# def club_signup():
#     data = request.json
#     club_name = data.get('Club Name')
#     college = data.get('College')
#     email = data.get('Email')
#     password = data.get('Password')

#     # Create user in Cognito
#     try:
#         cognito_client.sign_up(
#             ClientId=client_id,
#             Username=email,
#             Password=password,
#             UserAttributes=[
#                 {'Name': 'email', 'Value': email},
#                 {'Name': 'custom:club_name', 'Value': club_name},
#                 {'Name': 'custom:college', 'Value': college}
#             ]
#         )
#     except ClientError as e:
#         return jsonify({"error": str(e)}), 400

#     # Store club info in MySQL
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO CLUB_DETAILS (club_name, college, email) VALUES (%s, %s, %s)", (club_name, college, email))
#         conn.commit()
#     except mysql.connector.Error as err:
#         return jsonify({"error": str(err)}), 400
#     finally:
#         cursor.close()
#         conn.close()

#     return jsonify({"message": "Club signed up successfully"}), 201

# Club Signup
@app.route('/club/signup', methods=['POST'])
def club_signup():
    data = request.json
    club_name = data.get('Club Name')
    college = data.get('College')
    email = data.get('Email')
    password = data.get('Password')  # Use hashed passwords in production

    # Register user in AWS Cognito
    try:
        cognito_client.sign_up(
            ClientId=client_id,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'custom:club_name', 'Value': club_name},
                {'Name': 'custom:college', 'Value': college}
            ]
        )
    except ClientError as e:
        return jsonify({"error": str(e)}), 400

    # Insert into MySQL Users and CLUB_DETAILS tables
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert into Users table
        cursor.execute(
            "INSERT INTO Users (Email, PasswordHash, UserType) VALUES (%s, %s, %s)",
            (email, password, 'club')
        )
        conn.commit()

        # Get the UserID of the newly inserted user
        user_id = cursor.lastrowid

        # Insert into CLUB_DETAILS table
        cursor.execute(
            "INSERT INTO CLUB_DETAILS (UserID, ClubName, College) VALUES (%s, %s, %s)",
            (user_id, club_name, college)
        )
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Club signed up successfully"}), 201

# Sponsor Signup
@app.route('/company/signup', methods=['POST'])
def sponsor_signup():
    data = request.json
    company_name = data.get('Company name')
    industry = data.get('Industry')
    email = data.get('Email')
    password = data.get('Password')

    # Create user in Cognito
    try:
        cognito_client.sign_up(
            ClientId=client_id,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'custom:company_name', 'Value': company_name},
                {'Name': 'custom:industry', 'Value': industry}
            ]
        )
    except ClientError as e:
        return jsonify({"error": str(e)}), 400

    # Store sponsor info in MySQL
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO SPONSOR_DETAILS (company_name, industry, email) VALUES (%s, %s, %s)", (company_name, industry, email))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Sponsor signed up successfully"}), 201

# Verify email
# Email Verification
@app.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.json
    email = data.get('Email')
    confirmation_code = data.get('ConfirmationCode')

    # Confirm sign-up using Cognito
    try:
        cognito_client.confirm_sign_up(
            ClientId=client_id,
            Username=email,
            ConfirmationCode=confirmation_code
        )
        return jsonify({"message": "Email verified successfully"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400


# Club Login
@app.route('/club/login', methods=['POST'])
def club_login():
    data = request.json
    email = data.get('Email')
    password = data.get('Password')

    # Attempt login with Cognito
    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return jsonify({"message": "Club logged in successfully", "token": response['AuthenticationResult']['AccessToken']}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400

# Company Login
@app.route('/company/login', methods=['POST'])
def company_login():
    data = request.json
    email = data.get('Email')
    password = data.get('Password')

    # Attempt login with Cognito
    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return jsonify({"message": "Company logged in successfully", "token": response['AuthenticationResult']['AccessToken']}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400

# Password reset initiation
@app.route('/password/reset', methods=['POST'])
def initiate_password_reset():
    data = request.json
    email = data.get('Email')

    try:
        cognito_client.forgot_password(
            ClientId=client_id,
            Username=email
        )
        return jsonify({"message": "Password reset initiated"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400

# Confirm password reset
@app.route('/password/confirm_reset', methods=['POST'])
def confirm_password_reset():
    data = request.json
    email = data.get('Email')
    new_password = data.get('New Password')
    confirmation_code = data.get('Confirmation Code')

    try:
        cognito_client.confirm_forgot_password(
            ClientId=client_id,
            Username=email,
            ConfirmationCode=confirmation_code,
            Password=new_password
        )
        return jsonify({"message": "Password reset successful"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 400

# Club Create Event
@app.route('/club/create_event', methods=['POST'])
def create_event():
    data = request.json
    event_title = data.get('Event Title')
    date = data.get('Date')
    location = data.get('Location')
    amount = data.get('Amount')
    description = data.get('Description')
    image_url = data.get('Image URL')

    # Insert event details in MySQL
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO EVENT_DETAILS (event_title, date, location, amount, description, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
            (event_title, date, location, amount, description, image_url)
        )
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Event created successfully"}), 201

# Sponsorship Endpoint
@app.route('/company/sponsor', methods=['POST'])
def sponsorship():
    data = request.json
    event_id = data.get('event id')
    sponsorship_amount = data.get('Sponsorship Amount')
    message = data.get('Message')

    # Insert sponsorship details in MySQL
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO SPONSOR_CONFIRM (event_id, sponsorship_amount, message) VALUES (%s, %s, %s)",
            (event_id, sponsorship_amount, message)
        )
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Sponsorship added successfully"}), 201

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
