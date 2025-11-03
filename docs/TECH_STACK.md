# Crime Management System - Technical Stack

## 1. Backend Framework & Runtime
- **Language:** Python 3.14
- **Web Framework:** Flask 3.1.2
- **WSGI Server:** Werkzeug (development)
- **Template Engine:** Jinja2 3.1.6

## 2. Database & Storage
- **Database:** SQLite 3 (via Python's sqlite3 module)
- **Schema Management:** Raw SQL (schema.sql)
- **File Storage:** Local filesystem (development)

## 3. Frontend Technologies
- **HTML/CSS Framework:** Bootstrap 5.3.2 (via CDN)
- **JavaScript:** Vanilla JS (script.js)
- **Icons:** Font Awesome 6.0.0
- **CSS Features:**
  - Flexbox/Grid layouts
  - CSS transitions for cards
  - Responsive design breakpoints
  - Custom component styling

## 4. Dependencies (from requirements.txt)
```plaintext
Flask>=3.0.0
Werkzeug>=3.1.0
Jinja2>=3.1.2
itsdangerous>=2.2.0
click>=8.1.3
blinker>=1.9.0
MarkupSafe>=2.1.1
colorama>=0.4.6 (Windows-specific)
```

## 5. Project Structure
```plaintext
crime_management/
├── app.py               # Main Flask application
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── /static/           # Static assets
│   ├── style.css     # Custom styles
│   └── script.js     # Custom JavaScript
├── /templates/        # Jinja2 templates
│   ├── layout.html   # Base template
│   ├── landing.html  # Homepage
│   ├── cases.html    # Case listing
│   └── ...          # Other templates
└── /docs/            # Documentation
    └── PROJECT_OVERVIEW.md
```

## 6. Key Features Implementation

### Database Models
- Users & Roles
- FIRs (First Information Reports)
- Investigations
- Evidence Records

### API Routes
```plaintext
GET  /                 # Landing page
GET  /cases           # List all cases
POST /register        # Create new FIR
GET  /case/<id>       # View case details
POST /case/<id>       # Update case
GET  /reports         # View statistics
```

### UI Components
- Sliding feature cards
- Responsive data tables
- Form validation
- Flash messages
- Status badges
- Progress bars
- Responsive navigation

## 7. Development Tools
- **IDE/Editor:** VS Code
- **Version Control:** Git
- **Virtual Environment:** venv
- **Package Manager:** pip

## 8. Security Features
- CSRF Protection (via Flask-WTF, planned)
- SQL Parameter Binding
- Input Sanitization
- Role-Based Access Control (planned)

## 9. Deployment Requirements
### Minimum Hardware (Development)
- CPU: Any modern processor (2+ cores recommended)
- RAM: 2GB minimum
- Storage: 1GB for code, database, and assets

### Recommended Production Stack
- **Web Server:** Nginx or Apache
- **WSGI Server:** Gunicorn or uWSGI
- **Database:** PostgreSQL or MySQL
- **Cache:** Redis (for session storage)
- **Storage:** S3-compatible object storage
- **SSL/TLS:** Let's Encrypt certificates

## 10. Scalability Considerations
### Current Limitations
- SQLite (single-writer database)
- Local file storage
- No caching layer
- Single process/thread

### Recommended Upgrades for Scale
- Migration to PostgreSQL
- Connection pooling
- Redis caching
- Load balancing
- CDN for static assets
- Worker processes for background tasks

## 11. Testing Stack (Planned)
- **Unit Testing:** pytest
- **Coverage:** pytest-cov
- **UI Testing:** Selenium
- **Load Testing:** locust

## 12. Monitoring & Logging (Planned)
- **Application Logs:** Python logging
- **Error Tracking:** Sentry
- **Metrics:** Prometheus
- **Dashboard:** Grafana

## 13. CI/CD Pipeline (Recommended)
- **Platform:** GitHub Actions or Jenkins
- **Tests:** pytest
- **Linting:** flake8, black
- **Security:** bandit
- **Deploy:** Docker containers

## 14. Future Tech Considerations
- **Authentication:** Flask-Login or JWT
- **API Documentation:** Swagger/OpenAPI
- **Task Queue:** Celery + Redis
- **Search:** Elasticsearch
- **File Upload:** Flask-Upload with S3
- **Mobile:** Progressive Web App (PWA)

This tech stack is designed for rapid prototyping while maintaining a clear path to production scaling. Each component can be upgraded or replaced as requirements evolve.