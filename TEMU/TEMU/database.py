# database.py
import sqlite3
import os

def init_db():
    if not os.path.exists('data.db'):
        conn = sqlite3.connect('data.db')
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()