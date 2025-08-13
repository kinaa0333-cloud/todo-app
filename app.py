from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- Setup Database ---
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# --- Routes ---
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    if content:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    if request.method == 'POST':
        new_content = request.form['content']
        c.execute('UPDATE tasks SET content = ? WHERE id = ?', (new_content, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = c.fetchone()
        conn.close()
        return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Main ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
