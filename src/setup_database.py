import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
