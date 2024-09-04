import sqlite3

def setup_db():
    with sqlite3.connect('chatbot.db') as conn:
        cursor = conn.cursor()
        
        # Create the conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                bot_response TEXT NOT NULL
            )
        ''')
        
        print("Database setup complete.")

if __name__ == "__main__":
    setup_db()
