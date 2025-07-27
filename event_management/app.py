
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  date TEXT NOT NULL,
                  location TEXT NOT NULL)''')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        location = request.form['location']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO events (title, date, location) VALUES (?, ?, ?)", (title, date, location))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_event.html')

@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
