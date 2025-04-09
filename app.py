from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            rating REAL
        )
    ''')
    # Insert some sample movies if table is empty
    c.execute("SELECT COUNT(*) FROM movies")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO movies (title, rating) VALUES ('Inception', 4.5)")
        c.execute("INSERT INTO movies (title, rating) VALUES ('Interstellar', 4.8)")
        c.execute("INSERT INTO movies (title, rating) VALUES ('The Dark Knight', 4.9)")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = c.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/rate/<int:id>', methods=['POST'])
def rate(id):
    rating = request.form['rating']
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("UPDATE movies SET rating = ? WHERE id = ?", (rating, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
