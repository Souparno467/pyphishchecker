import sqlite3

# Define the database file name
DATABASE = 'phishing.db'

# Create the database and table
def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # SQL to create the `click_log` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS click_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    print(f"Database '{DATABASE}' and table 'click_log' created successfully.")

    # Close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
