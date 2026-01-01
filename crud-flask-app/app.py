from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
            (name, email, course)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id=?', (id,)
    ).fetchone()

    if request.method == 'POST':
        conn.execute(
            'UPDATE students SET name=?, email=?, course=? WHERE id=?',
            (
                request.form['name'],
                request.form['email'],
                request.form['course'],
                id
            )
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)