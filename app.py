from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        if conn is None:
            raise Exception("Database connection failed. Please check your MySQL credentials and database.")
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['password_hash'])
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        if conn is None:
            raise Exception("Database connection failed. Please check your MySQL credentials and database.")
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['password_hash'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.get_by_username(username):
            flash('Username already exists!')
            return redirect(url_for('register'))
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password!')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dashboard route
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# REST API: Get all tasks
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks WHERE user_id = %s', (current_user.id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)

# REST API: Add a task
@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    description = data.get('description')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, description, is_done) VALUES (%s, %s, %s)', (current_user.id, description, False))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task added!'}), 201

# REST API: Update a task (mark as done/undone)
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    data = request.get_json()
    is_done = data.get('is_done')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET is_done = %s WHERE id = %s AND user_id = %s', (is_done, task_id, current_user.id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task updated!'})

# REST API: Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, current_user.id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task deleted!'})

if __name__ == '__main__':
    app.run(debug=True) 