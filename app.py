from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE = 'phishing.db'

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS click_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            ip_address TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route for the landing page
@app.route('/')
def index():
    return render_template('index.html')

# Fake phishing page
@app.route('/phishing', methods=['GET', 'POST'])
def phishing():
    if request.method == 'POST':
        email = request.form.get('email')
        ip = request.remote_addr
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO click_log (email, ip_address, timestamp) VALUES (?, ?, ?)', (email, ip, timestamp))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback'))
    return render_template('phishing.html')

# Feedback page
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Admin panel for sending phishing emails
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        recipient_email = request.form.get('email')
        phishing_link = url_for('phishing', _external=True)
        send_phishing_email(recipient_email, phishing_link)
    return render_template('admin.html')

# Function to send phishing emails
def send_phishing_email(recipient, link):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "yourpassword"         # Replace with your email password
    subject = "Important: Verify Your Account"
    body = f"Click the link below to verify your account:\n\n{link}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

# Run the app
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
