from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit
import os
import random
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
socketio = SocketIO(app)

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        emailID TEXT UNIQUE,
        password TEXT
    )''')
    
    # Insert default admin user if not exists
    default_username = 'Admin'
    default_email = 'admin@dashboard.local'
    default_password = 'Password@123'
    hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (default_username,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, emailID, password) VALUES (?, ?, ?)",
                       (default_username, default_email, hashed_password))
    conn.commit()
    conn.close()

init_db()

# Function to validate user credentials
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False

# Route to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate credentials
        if validate_user(username, password):
            session['user'] = username  # Store user in session
            return redirect(url_for('manage'))  # Redirect to the manage page after successful login
        else:
            return render_template('login.html', error="Invalid credentials.")  # Show error if invalid credentials
    
    return render_template('login.html')  # If GET request, just render the login page

# Add User
@app.route('/add-user', methods=['POST'])
def add_user():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Hash the password and insert into the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, emailID, password) VALUES (?, ?, ?)",
                   (username, email, hashed_password))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 200

# Modify User
@app.route('/modify-user', methods=['POST'])
def modify_user():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    data = request.get_json()
    username = data.get('username')
    new_username = data.get('newUsername')
    new_email = data.get('newEmail')
    new_password = data.get('newPassword')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Prepare update statement
    update_values = []
    query = "UPDATE users SET "

    if new_username:
        query += "username = ?, "
        update_values.append(new_username)
    if new_email:
        query += "emailID = ?, "
        update_values.append(new_email)
    if new_password:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        query += "password = ?, "
        update_values.append(hashed_password)

    # Remove the trailing comma
    query = query.rstrip(', ')
    query += " WHERE username = ?"
    update_values.append(username)

    cursor.execute(query, tuple(update_values))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 200

# Delete User
@app.route('/delete-user/<username>', methods=['DELETE'])
def delete_user(username):
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 200

# Route to logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear session data on logout
    return redirect(url_for('login'))  # Redirect to login page after logout

# Directory where media files are stored
MEDIA_FOLDER = 'media'

# Ensure the media folder exists
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)

# Function to list files in the media folder (both images and videos)
def get_media_files():
    media_files = {'images': [], 'videos': []}
    for filename in os.listdir(MEDIA_FOLDER):
        filepath = os.path.join(MEDIA_FOLDER, filename)
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            media_files['images'].append(filename)
        elif filename.endswith('.mp4'):
            media_files['videos'].append(filename)
    return media_files

# Route to the main dashboard (index page)
@app.route('/')
def index():
    media_files = get_media_files()
    random.shuffle(media_files['images'])
    random.shuffle(media_files['videos'])
    return render_template('index.html', media_files=media_files)

# Route to the content management page (upload and manage files)
@app.route('/manage')
def manage():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    return render_template('manage.html')  # Render the manage page if logged in

# Route to upload a new media file (image or video)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    file = request.files.get('file')
    if file:
        file_path = os.path.join(MEDIA_FOLDER, file.filename)
        file.save(file_path)
        socketio.emit('media_uploaded', {'message': 'New media uploaded!'})
        return jsonify({'status': 'success', 'message': 'File uploaded successfully.'}), 200
    return jsonify({'status': 'error', 'message': 'No file provided.'}), 400

# Route to delete a media file
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    file_path = os.path.join(MEDIA_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        socketio.emit('media_deleted', {'message': f'{filename} deleted!'})
        return jsonify({'status': 'success', 'message': f'File {filename} deleted.'}), 200
    return jsonify({'status': 'error', 'message': 'File not found.'}), 404

# Route to serve media files (images and videos)
@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(MEDIA_FOLDER, filename)

# Route to get the list of media files
@app.route('/media-list', methods=['GET'])
def list_media():
    media_files = get_media_files()
    return jsonify({'media_files': media_files})

# Route to get the list of users
@app.route('/user-list', methods=['GET'])
def user_list():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, emailID FROM users")
    users = cursor.fetchall()
    conn.close()

    # Format the data into a dictionary
    user_data = []
    for user in users:
        user_data.append({
            'username': user[0],
            'email': user[1]
        })
    
    return jsonify({'users': user_data})

# Route to the media page (media management)
@app.route('/media')
def media_page():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    
    # Fetch media files from the media folder
    media_files = get_media_files()
    
    # Render the media.html page
    return render_template('media.html', media_files=media_files)



# Run the app with SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
