from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE_PATH = '/Users/vedanshkumar/Documents/Projects_sem5/AWS/Backend/details.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------CLUB TABLE-----------

# Create a new club
@app.route('/club', methods=['POST'])
def create_club():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO CLUB_DETAILS (CLUB_ID, CLUB_NAME, COLLEGE, EMAIL, PASSWORD)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['CLUB_ID'], data['CLUB_NAME'], data['COLLEGE'], data['EMAIL'], data['PASSWORD']))
        conn.commit()
    return jsonify({'message': 'Club created successfully'}), 201

# Read all clubs
@app.route('/clubs', methods=['GET'])
def get_clubs():
    conn = get_db_connection()
    clubs = conn.execute('SELECT * FROM CLUB_DETAILS').fetchall()
    conn.close()
    return jsonify([dict(row) for row in clubs])

# Update a club by ID
@app.route('/club/<club_id>', methods=['PUT'])
def update_club(club_id):
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE CLUB_DETAILS SET CLUB_NAME=?, COLLEGE=?, EMAIL=?, PASSWORD=?
            WHERE CLUB_ID=?
        ''', (data['CLUB_NAME'], data['COLLEGE'], data['EMAIL'], data['PASSWORD'], club_id))
        conn.commit()
    return jsonify({'message': 'Club updated successfully'})

# Delete a club by ID
@app.route('/club/<club_id>', methods=['DELETE'])
def delete_club(club_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM CLUB_DETAILS WHERE CLUB_ID=?', (club_id,))
        conn.commit()
    return jsonify({'message': 'Club deleted successfully'})

# -----------SPONSOR TABLE-----------

# Create a new sponsor
@app.route('/sponsor', methods=['POST'])
def create_sponsor():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO SPONSOR_DETAILS (SPONSOR_ID, SPONSOR_NAME, INDUSTRY, EMAIL, PASSWORD)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['SPONSOR_ID'], data['SPONSOR_NAME'], data['INDUSTRY'], data['EMAIL'], data['PASSWORD']))
        conn.commit()
    return jsonify({'message': 'Sponsor created successfully'}), 201

# Read all sponsors
@app.route('/sponsors', methods=['GET'])
def get_sponsors():
    conn = get_db_connection()
    sponsors = conn.execute('SELECT * FROM SPONSOR_DETAILS').fetchall()
    conn.close()
    return jsonify([dict(row) for row in sponsors])

# Update a sponsor by ID
@app.route('/sponsor/<sponsor_id>', methods=['PUT'])
def update_sponsor(sponsor_id):
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE SPONSOR_DETAILS SET SPONSOR_NAME=?, INDUSTRY=?, EMAIL=?, PASSWORD=?
            WHERE SPONSOR_ID=?
        ''', (data['SPONSOR_NAME'], data['INDUSTRY'], data['EMAIL'], data['PASSWORD'], sponsor_id))
        conn.commit()
    return jsonify({'message': 'Sponsor updated successfully'})

# Delete a sponsor by ID
@app.route('/sponsor/<sponsor_id>', methods=['DELETE'])
def delete_sponsor(sponsor_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM SPONSOR_DETAILS WHERE SPONSOR_ID=?', (sponsor_id,))
        conn.commit()
    return jsonify({'message': 'Sponsor deleted successfully'})

#-------EVENT_DETAILS TABLE-----------

# Create a new event
@app.route('/event', methods=['POST'])
def create_event():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO EVENT_DETAILS (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT, DESCRIPTION, IMAGE_URL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['EVENT_ID'], data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'], data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL']))
        conn.commit()
    return jsonify({'message': 'Event created successfully'}), 201

# Read all events
@app.route('/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM EVENT_DETAILS').fetchall()
    conn.close()
    return jsonify([dict(row) for row in events])

# Update an event by ID
@app.route('/event/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE EVENT_DETAILS SET CLUB_ID=?, EVENT_NAME=?, EVENT_DATE=?, LOCATION=?, SPONSOR_AMOUNT=?, DESCRIPTION=?, IMAGE_URL=?
            WHERE EVENT_ID=?
        ''', (data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'], data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL'], event_id))
        conn.commit()
    return jsonify({'message': 'Event updated successfully'})

# Delete an event by ID
@app.route('/event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM EVENT_DETAILS WHERE EVENT_ID=?', (event_id,))
        conn.commit()
    return jsonify({'message': 'Event deleted successfully'})

#---------SPONSOR CONFIRM-------------------
# Create a new sponsor confirmation
@app.route('/sponsor_confirm', methods=['POST'])
def create_sponsor_confirm():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO SPONSOR_CONFIRM (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['EVENT_ID'], data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'], data['SPONSOR_AMOUNT']))
        conn.commit()
    return jsonify({'message': 'Sponsor confirmation created successfully'}), 201

# Read all sponsor confirmations
@app.route('/sponsor_confirms', methods=['GET'])
def get_sponsor_confirms():
    conn = get_db_connection()
    sponsor_confirms = conn.execute('SELECT * FROM SPONSOR_CONFIRM').fetchall()
    conn.close()
    return jsonify([dict(row) for row in sponsor_confirms])

# Update a sponsor confirmation by event ID
@app.route('/sponsor_confirm/<event_id>', methods=['PUT'])
def update_sponsor_confirm(event_id):
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE SPONSOR_CONFIRM SET CLUB_ID=?, EVENT_NAME=?, EVENT_DATE=?, LOCATION=?, SPONSOR_AMOUNT=?
            WHERE EVENT_ID=?
        ''', (data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'], data['SPONSOR_AMOUNT'], event_id))
        conn.commit()
    return jsonify({'message': 'Sponsor confirmation updated successfully'})

# Delete a sponsor confirmation by event ID
@app.route('/sponsor_confirm/<event_id>', methods=['DELETE'])
def delete_sponsor_confirm(event_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM SPONSOR_CONFIRM WHERE EVENT_ID=?', (event_id,))
        conn.commit()
    return jsonify({'message': 'Sponsor confirmation deleted successfully'})

#---------REDUNDENT_DETAILS TABLE-------------
# Create a new redundant detail
@app.route('/redundant_detail', methods=['POST'])
def create_redundant_detail():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO REDUNDENT_DETAILS (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT, DESCRIPTION, IMAGE_URL)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['EVENT_ID'], data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'], data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL']))
        conn.commit()
    return jsonify({'message': 'Redundant detail created successfully'}), 201

# Read all redundant details
@app.route('/redundant_details', methods=['GET'])
def get_redundant_details():
    conn = get_db_connection()
    redundant_details = conn.execute('SELECT * FROM REDUNDENT_DETAILS').fetchall()
    conn.close()
    return jsonify([dict(row) for row in redundant_details])

# Update a redundant detail by event ID
@app.route('/redundant_detail/<event_id>', methods=['PUT'])
def update_redundant_detail(event_id):
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE REDUNDENT_DETAILS SET CLUB_ID=?, EVENT_NAME=?, EVENT_DATE=?, LOCATION=?, SPONSOR_AMOUNT=?, DESCRIPTION=?, IMAGE_URL=?
            WHERE EVENT_ID=?
        ''', (data['CLUB_ID'], data['EVENT_NAME'], data['EVENT_DATE'], data['LOCATION'], data['SPONSOR_AMOUNT'], data['DESCRIPTION'], data['IMAGE_URL'], event_id))
        conn.commit()
    return jsonify({'message': 'Redundant detail updated successfully'})

# Delete a redundant detail by event ID
@app.route('/redundant_detail/<event_id>', methods=['DELETE'])
def delete_redundant_detail(event_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM REDUNDENT_DETAILS WHERE EVENT_ID=?', (event_id,))
        conn.commit()
    return jsonify({'message': 'Redundant detail deleted successfully'})
