# Crime Management System — Project Overview

## Introduction

The Crime Management System (CMS) is a lightweight web application built with Python and Flask for recording, tracking, and managing criminal complaints (FIRs), assignments, investigations, and evidence. It is designed as a prototyping skeleton that can be extended into a production system with authentication, stronger storage, and analytics.

Goal: provide a single source of truth for cases, enable assignment and investigation workflows, and produce actionable reports.

---

## How to use (Quick)

1. Create and activate a Python virtual environment in the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Initialize the database (creates `cms.db` from `schema.sql`):

```powershell
python -c "from app import init_db; init_db()"
```

4. Run the app (development mode):

```powershell
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000 in your browser.

---

## Very Important Code Snippets

Below are the most important code snippets to understand how core functionality is implemented. You can copy these into other projects or use them as the base for further development.

### 1) Database initialization (init_db)

```python
# app.py — init_db helper
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
```

Purpose: creates tables and seed roles. Use this to reset or create the initial database.


### 2) Register FIR (important fields: location, priority)

```python
# app.py — register_fir route
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
```

Why it matters: this captures the essential case metadata (location, priority) required for filtering and reporting.


### 3) Case detail and update (assign, status change, add investigation note)

```python
# app.py — case_detail route
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
    return render_template('case_detail.html', case=case, officers=officers, investigations=investigations, statuses=['Open', 'Assigned', 'In Progress', 'Closed'])
```

Why it matters: assignment, status transitions, and the investigation timeline are core to the operational workflow.


### 4) Querying/filtering cases (used by `view_cases`)

```python
# app.py — view_cases route (filter by query params)
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
```

Why it matters: this provides the filtering functionality users asked for: status, priority, location.

---

## Use Cases

1. Citizen files a complaint (FIR) at a police station or online. The clerk records the FIR with location and priority.
2. Admin assigns the FIR to an available officer (assignment triggers status change to "Assigned").
3. Officer visits the scene, adds investigation notes and evidence entries, and updates status through the lifecycle.
4. Admin generates reports to identify hotspots and resource needs.
5. Filtering and querying produce targeted lists (e.g., all High-priority cases in a neighborhood).

---

## Feature Scope (Current & Next)

Included in this skeleton (current):
- FIR registration form (title, complainant, description, location, priority)
- Case listing with filters (status, priority, location)
- Case detail view with assignment and investigation updates
- Simple reports (counts by status/priority/location)
- Responsive UI with Bootstrap and sliding cards on the landing page

Planned / Recommended (next enhancements):
- Authentication & RBAC (Flask-Login, role checks per route)
- Evidence file upload (secure storage, S3 or encrypted local store)
- Geo-coordinates + map-based hotspot visualization
- API endpoints (JSON) and CSV/PDF exports for reports
- Notifications (email/SMS) for deadlines and assignments
- Move to PostgreSQL for production and add migrations (Alembic)
- Audit logs and advanced access control rules

---

## Where to find important files in repo

- `app.py` — main Flask app and route handlers
- `schema.sql` — database schema and seed roles
- `templates/` — Jinja2 HTML templates (landing, register, cases, case_detail, reports)
- `static/` — CSS and JS (Bootstrap used via CDN)
- `requirements.txt` — Python dependencies

---

## Next steps (if you want me to proceed)

- Add authentication and RBAC (recommended next step).  
- Implement file uploads for evidence (requires secure storage planning).  
- Add API endpoints and a simple export-to-CSV report.  

If you want, I can commit this doc to the repo and add a short README entry linking to it. Would you like me to save it now and/or open the server to show the UI live?