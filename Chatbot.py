import tkinter as tk
from tkinter import scrolledtext
import sqlite3
import datetime
import socket
import requests

def connect_db():
    return sqlite3.connect('chatbot.db')

def store_conversation(user_input, bot_response):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO conversations (user_input, bot_response)
            VALUES (?, ?)
        ''', (user_input, bot_response))
        conn.commit()

def get_bot_response(user_input):
    user_input = user_input.lower()
    
    if 'time' in user_input:
        return get_current_time()
    elif 'location' in user_input:
        return get_location()
    elif 'date' in user_input:
        return get_current_date()
    elif 'weather' in user_input:
        return "I’m not able to fetch weather data right now, but you can check your local weather app!"
    elif 'joke' in user_input:
        return get_joke()
    elif 'quote' in user_input:
        return get_quote()
    elif 'how are you' in user_input:
        return "I’m just a bot, but I’m doing great! How can I assist you today?"
    elif 'what is your name' in user_input:
        return "I am a chatbot created by OpenAI. What's your name?"
    elif 'bye' in user_input:
        return "Goodbye! Have a wonderful day!"
    else:
        return "I’m not sure how to respond to that. Can you ask something else?"

def get_current_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')}."

def get_current_date():
    today = datetime.date.today()
    return f"Today's date is {today.strftime('%Y-%m-%d')}."

def get_location():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Use ipinfo.io API to get location from IP address
        response = requests.get(f'https://ipinfo.io/{ip_address}/json?token=2af7500d24d04d')
        data = response.json()
        
        city = data.get('city', 'unknown city')
        region = data.get('region', 'unknown region')
        country = data.get('country', 'unknown country')
        
        return f"The IP address of this machine is {ip_address}. Location: {city}, {region}, {country}."
    except Exception as e:
        return "Unable to retrieve location information."

def get_joke():
    return "Why don't scientists trust atoms? Because they make up everything!"

def get_quote():
    return "“The only way to do great work is to love what you do.” – Steve Jobs"

def send_message():
    user_input = entry.get()
    if user_input.strip() == '':
        return  # Ignore empty input
    
    bot_response = get_bot_response(user_input)
    if user_input.lower() == 'bye':
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"You: {user_input}\nBot: {bot_response}\n")
        text_area.config(state=tk.DISABLED)
        store_conversation(user_input, bot_response)
        root.quit()
    else:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"You: {user_input}\nBot: {bot_response}\n")
        text_area.config(state=tk.DISABLED)
        store_conversation(user_input, bot_response)
        entry.delete(0, tk.END)
        text_area.yview(tk.END)  # Auto-scroll to the bottom

# Create the main window
root = tk.Tk()
root.title("Chatbot")

# Create a text area for chat history
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create an entry widget for user input
entry = tk.Entry(root)
entry.pack(padx=10, pady=10, fill=tk.X, side=tk.LEFT, expand=True)

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.RIGHT)

# Run the GUI event loop
root.mainloop()
