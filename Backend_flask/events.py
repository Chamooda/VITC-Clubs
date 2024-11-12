from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/Users/vedanshkumar/Documents/Projects_sem5/AWS/Backend/details.db')  # Replace with your database path
    conn.row_factory = sqlite3.Row
    return conn

# 1. Add Event
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    event_id = data.get("event_id")
    club_id = data.get("club_id")
    event_name = data.get("event_name")
    event_date = data.get("event_date")
    location = data.get("location")
    sponsor_amount = data.get("sponsor_amount")
    description = data.get("description")
    image_url = data.get("image_url")
    
    insert_query = '''
        INSERT INTO EVENT_DETAILS (EVENT_ID, CLUB_ID, EVENT_NAME, EVENT_DATE, LOCATION, SPONSOR_AMOUNT, DESCRIPTION, IMAGE_URL)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(insert_query, (event_id, club_id, event_name, event_date, location, sponsor_amount, description, image_url))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()
    return jsonify({"message": "Event added successfully"}), 201

# 2. Get All Events
@app.route('/event_details', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENT_DETAILS")
    events = cursor.fetchall()
    conn.close()
    event_list = [dict(row) for row in events]
    return jsonify(event_list)

# 3. Get Event by ID
@app.route('/event_details/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENT_DETAILS WHERE EVENT_ID = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(dict(event))

# 4. Update Event by ID
@app.route('/event_details/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    fields = ["club_id", "event_name", "event_date", "location", "sponsor_amount", "description", "image_url"]
    values = [data.get(field) for field in fields]
    
    update_query = '''
        UPDATE EVENT_DETAILS
        SET CLUB_ID = ?, EVENT_NAME = ?, EVENT_DATE = ?, LOCATION = ?, SPONSOR_AMOUNT = ?, DESCRIPTION = ?, IMAGE_URL = ?
        WHERE EVENT_ID = ?
    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(update_query, (*values, event_id))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Event updated successfully"}), 200

# 5. Delete Event by ID
@app.route('/event_details/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM EVENT_DETAILS WHERE EVENT_ID = ?", (event_id,))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Event deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
