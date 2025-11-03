-- Schema for a minimal Crime Management System (SQLite)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT,
    role_id INTEGER,
    password_hash TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS firs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    complainant_name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')) DEFAULT 'Medium',
    assigned_to INTEGER,
    status TEXT DEFAULT 'Open' CHECK(status IN ('Open', 'Assigned', 'In Progress', 'Closed')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

-- Insert default roles
INSERT OR IGNORE INTO roles (name, description) VALUES 
    ('admin', 'System Administrator'),
    ('officer', 'Police Officer'),
    ('clerk', 'Station Clerk');

CREATE TABLE IF NOT EXISTS criminals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    alias TEXT,
    dob DATE,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fir_id INTEGER,
    description TEXT,
    stored_at TEXT,
    FOREIGN KEY (fir_id) REFERENCES firs(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS investigations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fir_id INTEGER NOT NULL,
    officer TEXT,
    notes TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fir_id) REFERENCES firs(id) ON DELETE CASCADE
);
