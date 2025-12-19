from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import secrets
import json
import os

app = Flask(__name__)
# NOTE: keep a secure secret in production (env var or config)
app.secret_key = 'dev-secret-change-me'

# Persistent store for institutes (simple JSON file for development)
INSTITUTES_FILE = os.path.join(os.path.dirname(__file__), 'institutes.json')

def load_institutes():
    try:
        with open(INSTITUTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_institutes():
    os.makedirs(os.path.dirname(INSTITUTES_FILE), exist_ok=True)
    with open(INSTITUTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(app.config['INSTITUTES'], f, indent=2, ensure_ascii=False)

# load at startup
app.config['INSTITUTES'] = load_institutes()

# Default credentials for roles (development only - replace with secure store)
CREDENTIALS = {
    'auditor': '1234',
    'admin': 'adminpass',
    'chancellor': 'chancellorpass',
    'vice_chancellor': 'vcpass',
    'director': 'directorpass',
    'iqac_coordinators': 'iqacpass',
}

ROLE_DISPLAY = {
    'auditor': 'Auditor',
    'admin': 'Admin',
    'chancellor': 'Chancellor',
    'vice_chancellor': 'Vice Chancellor',
    'director': 'Director',
    'iqac_coordinators': 'IQAC Coordinators',
}

@app.context_processor
def inject_now():
    return {
        'current_year': datetime.now().year,
        'is_admin': session.get('is_admin', False),
        'role': session.get('role', None),
        'selected_institute': session.get('selected_institute', None),
        'institutes': app.config['INSTITUTES'],
        'ROLE_DISPLAY': ROLE_DISPLAY
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    # Generate a fresh captcha on GET
    if request.method == "GET":
        session['captcha'] = ''.join(secrets.choice('0123456789') for _ in range(5))

    if request.method == "POST":
        login_by = request.form.get("login_by")
        password = request.form.get("password")
        captcha = request.form.get("captcha")
        expected = session.get('captcha')

        # Verify credentials for any configured role
        expected_password = CREDENTIALS.get(login_by)
        if expected_password and password == expected_password and captcha == expected:
            # Admin gets special privileges
            if login_by == 'admin':
                session['is_admin'] = True
                session['selected_institute'] = None
                session.pop('captcha', None)
                return redirect(url_for('admin'))

            # Non-admin roles
            session.pop('is_admin', None)
            session['selected_institute'] = None
            session['role'] = login_by
            message = f"Login Successful ({ROLE_DISPLAY.get(login_by, login_by)})"
            session.pop('captcha', None)
            return redirect(url_for('dashboard'))

        message = "Invalid Credentials"
        # rotate captcha after a failed attempt
        session['captcha'] = ''.join(secrets.choice('0123456789') for _ in range(5))
    # Ensure a captcha exists before rendering
    if 'captcha' not in session:
        session['captcha'] = ''.join(secrets.choice('0123456789') for _ in range(5))

    return render_template("login.html", message=message)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Only allow access to admins
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('institute_name', '').strip()
        if name:
            # avoid duplicates
            if name not in app.config['INSTITUTES']:
                app.config['INSTITUTES'].append(name)
                save_institutes()
    return render_template('admin.html', institutes=app.config['INSTITUTES'])


@app.route('/dashboard')
def dashboard():
    # Allow access to any logged-in role or admin
    if not (session.get('is_admin') or session.get('role')):
        return redirect(url_for('login'))
    return render_template('dashboard.html', role=session.get('role'), institutes=app.config['INSTITUTES'])

@app.route('/select_institute', methods=['POST'])
def select_institute():
    # Allow admins and other logged-in roles to select a current institute
    if not (session.get('is_admin') or session.get('role')):
        return redirect(url_for('login'))
    inst = request.form.get('institute')
    if inst:
        session['selected_institute'] = inst
    # Send back to the page that submitted the form or to dashboard
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/remove_institute', methods=['POST'])
def remove_institute():
    # only admins may remove
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    inst = request.form.get('institute')
    if inst and inst in app.config['INSTITUTES']:
        try:
            app.config['INSTITUTES'].remove(inst)
            save_institutes()
        except ValueError:
            pass
        if session.get('selected_institute') == inst:
            session['selected_institute'] = None
    return redirect(request.referrer or url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
