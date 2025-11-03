from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'cms.db')

app = Flask(__name__)
app.secret_key = 'change-me-for-production'

# Helper function to get status and priority colors for badges
def get_status_color(status):
    return {
        'Open': 'info',
        'Assigned': 'secondary',
        'In Progress': 'warning',
        'Closed': 'success'
    }.get(status, 'secondary')

def get_priority_color(priority):
    return {
        'High': 'danger',
        'Medium': 'warning',
        'Low': 'success'
    }.get(priority, 'secondary')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the SQLite database using schema.sql."""
    schema_path = os.path.join(BASE_DIR, 'schema.sql')
    if not os.path.exists(schema_path):
        raise FileNotFoundError('schema.sql not found')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print('Database initialized at', DB_PATH)


@app.route('/')
def index():
    conn = get_db_connection()
    recent_cases = conn.execute('''
        SELECT id, title, status, priority, updated_at 
        FROM firs 
        ORDER BY updated_at DESC 
        LIMIT 5
    ''').fetchall()
    
    # Convert to list of dicts and add colors
    cases = []
    for case in recent_cases:
        cases.append({
            'id': case['id'],
            'title': case['title'],
            'status': case['status'],
            'status_color': get_status_color(case['status']),
            'priority': case['priority'],
            'priority_color': get_priority_color(case['priority']),
            'updated_at': case['updated_at']
        })
    
    conn.close()
    return render_template('landing.html', recent_cases=cases)

@app.route('/cases')
def view_cases():
    status = request.args.get('status')
    priority = request.args.get('priority')
    location = request.args.get('location')
    
    query = '''
        SELECT f.*, u.full_name as officer_name 
        FROM firs f 
        LEFT JOIN users u ON f.assigned_to = u.id 
        WHERE 1=1
    '''
    params = []
    
    if status:
        query += ' AND f.status = ?'
        params.append(status)
    if priority:
        query += ' AND f.priority = ?'
        params.append(priority)
    if location:
        query += ' AND f.location LIKE ?'
        params.append(f'%{location}%')
        
    query += ' ORDER BY f.updated_at DESC'
    
    conn = get_db_connection()
    cases = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('cases.html', cases=cases)

@app.route('/register', methods=['GET', 'POST'])
def register_fir():
    if request.method == 'POST':
        title = request.form.get('title')
        complainant = request.form.get('complainant')
        description = request.form.get('description')
        location = request.form.get('location')
        priority = request.form.get('priority', 'Medium')
        
        if not title or not complainant or not location:
            flash('Title, complainant name, and location are required', 'danger')
            return redirect(url_for('register_fir'))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO firs (
                title, complainant_name, description, location, 
                priority, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (title, complainant, description, location, priority, 'Open'))
        conn.commit()
        conn.close()
        
        flash('FIR registered successfully', 'success')
        return redirect(url_for('view_cases'))

    return render_template('register_fir.html', priorities=['High', 'Medium', 'Low'])

@app.route('/case/<int:case_id>', methods=['GET', 'POST'])
def case_detail(case_id):
    conn = get_db_connection()
    if request.method == 'POST':
        status = request.form.get('status')
        assigned_to = request.form.get('assigned_to')
        notes = request.form.get('notes')
        
        conn.execute('''
            UPDATE firs 
            SET status = ?, assigned_to = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (status, assigned_to, case_id))
        
        if notes:
            conn.execute('''
                INSERT INTO investigations (fir_id, officer, notes) 
                VALUES (?, ?, ?)
            ''', (case_id, assigned_to, notes))
            
        conn.commit()
        flash('Case updated successfully', 'success')
        
    case = conn.execute('SELECT * FROM firs WHERE id = ?', (case_id,)).fetchone()
    officers = conn.execute('SELECT id, full_name FROM users WHERE role_id = 2').fetchall()
    investigations = conn.execute('''
        SELECT i.*, u.full_name 
        FROM investigations i 
        LEFT JOIN users u ON i.officer = u.id 
        WHERE i.fir_id = ? 
        ORDER BY i.updated_at DESC
    ''', (case_id,)).fetchall()
    
    conn.close()
    return render_template('case_detail.html', 
                         case=case, 
                         officers=officers, 
                         investigations=investigations,
                         statuses=['Open', 'Assigned', 'In Progress', 'Closed'])

@app.route('/reports')
def reports():
    conn = get_db_connection()
    
    # Get case statistics
    stats = {}
    stats['total'] = conn.execute('SELECT COUNT(*) as count FROM firs').fetchone()['count']
    stats['by_status'] = conn.execute('''
        SELECT status, COUNT(*) as count 
        FROM firs 
        GROUP BY status
    ''').fetchall()
    stats['by_priority'] = conn.execute('''
        SELECT priority, COUNT(*) as count 
        FROM firs 
        GROUP BY priority
    ''').fetchall()
    stats['by_location'] = conn.execute('''
        SELECT location, COUNT(*) as count 
        FROM firs 
        GROUP BY location 
        ORDER BY count DESC 
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    return render_template('reports.html', stats=stats)


if __name__ == '__main__':
    # If DB doesn't exist, initialize it automatically for convenience.
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
