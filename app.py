from flask import Flask, render_template, request, redirect, url_for, session, flash, g, make_response
import sqlite3
import os
import subprocess
import hashlib
import re

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.urandom(24)

DATABASE = 'database.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = hashlib.sha256('admin_password'.encode()).hexdigest() # Change this to a strong password in production!

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        # Create table directly instead of reading from schema.sql
        db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script TEXT NOT NULL,
                target TEXT NOT NULL,
                parameters TEXT,
                output TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            session['logged_in'] = True
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

def sanitize_input(input_str):
    """Basic input sanitization to prevent command injection"""
    # Remove dangerous characters
    dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>', '"', "'"]
    for char in dangerous_chars:
        input_str = input_str.replace(char, '')
    return input_str.strip()

@app.route('/execute', methods=['POST'])
def execute_script():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    target = request.form['target']
    script = request.form['script']
    params = request.form.get('params', '')
    output = ''

    # Basic input validation
    if not target or not script:
        flash('Target and script are required.')
        return redirect(url_for('index'))

    # Sanitize inputs
    target = sanitize_input(target)
    params = sanitize_input(params)

    # Validate target format (basic IP/domain validation)
    if not re.match(r'^[a-zA-Z0-9.-]+$', target):
        output = 'Invalid target format. Only alphanumeric characters, dots, and hyphens are allowed.'
        return render_template('dashboard.html', output=output, target=target, script=script, params=params)

    try:
        if script == 'nmap':
            # Basic nmap scan with limited options for security
            cmd = ['nmap', '-sT', '-O', target]
            if params:
                # Only allow safe nmap parameters
                safe_params = ['-p', '-sV', '-A', '-T4', '-T3', '-T2', '-T1']
                param_list = params.split()
                for param in param_list:
                    if param in safe_params or param.startswith('-p'):
                        cmd.append(param)
        elif script == 'whois':
            cmd = ['whois', target]
        elif script == 'dig':
            cmd = ['dig', target]
        elif script == 'traceroute':
            cmd = ['traceroute', target]
        elif script == 'hydra':
            # WARNING: Hydra can be dangerous. Use with extreme caution and only on authorized systems.
            # This is a very basic implementation - in production, you'd want much more control
            output = 'Hydra functionality disabled for security reasons. Please implement with proper authorization checks.'
            cmd = []
        else:
            output = 'Unknown script.'
            cmd = []

        if cmd:
            # Set timeout to prevent hanging
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            if result.returncode != 0:
                output += f"\nCommand exited with code: {result.returncode}"

    except subprocess.TimeoutExpired:
        output = "Command timed out after 30 seconds."
    except subprocess.CalledProcessError as e:
        output = f"Error executing script: {e}\n{e.stdout}\n{e.stderr}"
    except FileNotFoundError:
        output = f"Error: {script} command not found. Make sure it's installed and in your PATH."
    except Exception as e:
        output = f"An unexpected error occurred: {e}"

    # Save to history
    try:
        db = get_db()
        db.execute('INSERT INTO history (script, target, parameters, output) VALUES (?, ?, ?, ?)',
                   (script, target, params, output))
        db.commit()
    except Exception as e:
        flash(f'Error saving to history: {e}')

    return render_template('dashboard.html', output=output, target=target, script=script, params=params)

@app.route('/history')
def history():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('SELECT id, script, target, timestamp FROM history ORDER BY timestamp DESC')
    history_entries = cur.fetchall()
    return render_template('history.html', history_entries=history_entries)

@app.route('/history/<int:entry_id>')
def view_history_entry(entry_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('SELECT * FROM history WHERE id = ?', (entry_id,))
    entry = cur.fetchone()
    if entry:
        return render_template('history_detail.html', entry=entry)
    else:
        flash('History entry not found.')
        return redirect(url_for('history'))

@app.route('/download_report/<int:entry_id>')
def download_report(entry_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('SELECT script, target, output, timestamp FROM history WHERE id = ?', (entry_id,))
    entry = cur.fetchone()
    if entry:
        report_content = f"Script: {entry['script']}\nTarget: {entry['target']}\nTimestamp: {entry['timestamp']}\n\nOutput:\n{entry['output']}"
        response = make_response(report_content)
        response.headers["Content-Disposition"] = f"attachment; filename=report_{entry_id}.txt"
        response.mimetype = "text/plain"
        return response
    else:
        flash('History entry not found.')
        return redirect(url_for('history'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)


