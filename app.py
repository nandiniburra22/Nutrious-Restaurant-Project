from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import sqlite3
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Your app password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Database connection function
def connect_db():
    return sqlite3.connect('contacts.db')

# Create table function
def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

# Route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML page

# Route to handle form submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    # Validate form data
    if not all([name, email, phone, message]):
        return jsonify({'message': 'All fields are required!'}), 400

    try:
        # Insert the form data into the SQLite database
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contact (name, email, phone, message) VALUES (?, ?, ?, ?)", 
                           (name, email, phone, message))
            conn.commit()
    except Exception as e:
        return jsonify({'message': f'Failed to save contact: {e}'}), 500

    # Send notification email
    if not send_email(name, email,phone, message):
        return jsonify({'message': 'Failed to send notification email!'}), 500

    # Print received data for debugging
    print("Received data - Name: {name}, Email: {email}, Phone: {phone}, Message: {message}")

    return jsonify("Thank you for submitting the form!")

# Function to send email using Flask-Mail
def send_email(name, email, phone, message):
    try:
        msg = Message('New Contact Form Submission',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['skrestaurant24@gmail.com'])  # Replace with the recipient's email
        msg.body = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'

        # Send email
        mail.send(msg)
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Start the Flask server
if __name__ == '__main__':
    create_table()  # Create the table when the server starts
    app.run(debug=True)
