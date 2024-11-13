from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='DB_HOST',
        user='DB_USER',
        password='DB_PASSWORD',
        database='DB_NAME'
    )

# Generic function for executing SQL commands
def execute_query(query, params=()):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        connection.commit()
        return cursor.lastrowid if cursor.rowcount > 0 else None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# Endpoint to insert data into CLUB_DETAILS
@app.route('/club', methods=['POST'])
def insert_club():
    data = request.json
    query = '''INSERT INTO CLUB_DETAILS (CLUB_ID, CLUB_NAME, COLLEGE, EMAIL, PASSWORD)
               VALUES (%s, %s, %s, %s, %s)'''
    execute_query(query, (data['CLUB_ID'], data['CLUB_NAME'], data['COLLEGE'], data['EMAIL'], data['PASSWORD']))
    return jsonify({"message": "Club inserted successfully"}), 201

# Endpoint to update data in CLUB_DETAILS
@app.route('/club/<club_id>', methods=['PUT'])
def update_club(club_id):
    data = request.json
    query = '''UPDATE CLUB_DETAILS SET CLUB_NAME = %s, COLLEGE = %s, EMAIL = %s, PASSWORD = %s
               WHERE CLUB_ID = %s'''
    execute_query(query, (data['CLUB_NAME'], data['COLLEGE'], data['EMAIL'], data['PASSWORD'], club_id))
    return jsonify({"message": "Club updated successfully"})

# Endpoint to delete data from CLUB_DETAILS
@app.route('/club/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    query = "DELETE FROM CLUB_DETAILS WHERE CLUB_ID = %s"
    execute_query(query, (club_id,))
    return jsonify({"message": "Club deleted successfully"})

# Repeat similar endpoints for SPONSOR_DETAILS
@app.route('/sponsor', methods=['POST'])
def insert_sponsor():
    data = request.json
    query = '''INSERT INTO SPONSOR_DETAILS (SPONSOR_ID, SPONSOR_NAME, INDUSTRY, EMAIL, PASSWORD)
               VALUES (%s, %s, %s, %s, %s)'''
    execute_query(query, (data['SPONSOR_ID'], data['SPONSOR_NAME'], data['INDUSTRY'], data['EMAIL'], data['PASSWORD']))
    return jsonify({"message": "Sponsor inserted successfully"}), 201

@app.route('/sponsor/<sponsor_id>', methods=['PUT'])
def update_sponsor(sponsor_id):
    data = request.json
    query = '''UPDATE SPONSOR_DETAILS SET SPONSOR_NAME = %s, INDUSTRY = %s, EMAIL = %s, PASSWORD = %s
               WHERE SPONSOR_ID = %s'''
    execute_query(query, (data['SPONSOR_NAME'], data['INDUSTRY'], data['EMAIL'], data['PASSWORD'], sponsor_id))
    return jsonify({"message": "Sponsor updated successfully"})

@app.route('/sponsor/<sponsor_id>', methods=['DELETE'])
def delete_sponsor(sponsor_id):
    query = "DELETE FROM SPONSOR_DETAILS WHERE SPONSOR_ID = %s"
    execute_query(query, (sponsor_id,))
    return jsonify({"message": "Sponsor deleted successfully"})

# Repeat similar endpoints for EVENT_DETAILS
@app.route('/event', methods=['POST'])
def insert_event():
    data = request.json
    query = '''INSERT INTO EVENT_DETAILS (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT, DESCRIPTION, IMAGE_URL)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    execute_query(query, (data['EVENT_ID'], data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'],
                          data['LOCATION'], data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL']))
    return jsonify({"message": "Event inserted successfully"}), 201

@app.route('/event/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    query = '''UPDATE EVENT_DETAILS SET CLUB_ID = %s, EVENT_NAME = %s, EVENT_DATE = %s, LOCATION = %s,
               SPONSOR_AMOUNT = %s, DESCRIPTION = %s, IMAGE_URL = %s WHERE EVENT_ID = %s'''
    execute_query(query, (data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'],
                          data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL'], event_id))
    return jsonify({"message": "Event updated successfully"})

@app.route('/event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    query = "DELETE FROM EVENT_DETAILS WHERE EVENT_ID = %s"
    execute_query(query, (event_id,))
    return jsonify({"message": "Event deleted successfully"})

# Repeat similar endpoints for SPONSOR_CONFIRM
@app.route('/sponsor_confirm', methods=['POST'])
def insert_sponsor_confirm():
    data = request.json
    query = '''INSERT INTO SPONSOR_CONFIRM (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT)
               VALUES (%s, %s, %s, %s, %s, %s)'''
    execute_query(query, (data['EVENT_ID'], data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'],
                          data['LOCATION'], data['SPONSOR_AMOUNT']))
    return jsonify({"message": "Sponsor confirmation inserted successfully"}), 201

@app.route('/sponsor_confirm/<event_id>', methods=['DELETE'])
def delete_sponsor_confirm(event_id):
    query = "DELETE FROM SPONSOR_CONFIRM WHERE EVENT_ID = %s"
    execute_query(query, (event_id,))
    return jsonify({"message": "Sponsor confirmation deleted successfully"})

# Repeat similar endpoints for REDUNDENT_DETAILS
@app.route('/redundent', methods=['POST'])
def insert_redundent():
    data = request.json
    query = '''INSERT INTO REDUNDENT_DETAILS (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT, DESCRIPTION, IMAGE_URL)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    execute_query(query, (data['EVENT_ID'], data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'],
                          data['LOCATION'], data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL']))
    return jsonify({"message": "Redundent detail inserted successfully"}), 201

@app.route('/redundent/<event_id>', methods=['DELETE'])
def delete_redundent(event_id):
    query = "DELETE FROM REDUNDENT_DETAILS WHERE EVENT_ID = %s"
    execute_query(query, (event_id,))
    return jsonify({"message": "Redundent detail deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
