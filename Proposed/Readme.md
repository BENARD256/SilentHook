Got it, here it is:

---

# DBBD — Developer README

## What This App Does
A Flask-based honeytoken/canary trap system. It deploys deceptive bait files, URLs, and database triggers that silently alert the team the moment an unauthorised user accesses them.

Purpose 
am proposing the use of this struture so as to enable the implemenation and intregation of the system with caching system redis .This intergation calls for use of a containerization i.e docker so as to enable easy setup and  initailizaton
---

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask |
| Database | PostgreSQL + SQLAlchemy |
| Cache | Redis (Flask-Caching) |
| Auth | JWT (Flask-JWT-Extended) |
| Server | Gunicorn + Nginx |
| Container | Docker + Docker Compose |

---

## Folder Structure
```
DBBD/
├── app/
│   ├── __init__.py         # App factory — create_app() lives here
│   ├── extensions.py       # db, cache, jwt — init once, import everywhere
│   ├── config.py           # DevelopmentConfig / ProductionConfig
│   │
│   ├── models/             # One file per database table
│   │   ├── user.py         # Users
│   │   ├── bait.py         # Baits
│   │   ├── trigger.py      # Triggers
│   │   ├── alert.py        # Alerts + Alert_history
│   │   └── event.py        # Watcher_events + Mysql_events
│   │
│   ├── blueprints/         # One folder per feature area
│   │   ├── auth/           # Login, register, JWT routes
│   │   ├── baits/          # Bait CRUD
│   │   ├── triggers/       # Trigger management
│   │   ├── alerts/         # Callback handling
│   │   └── views/          # HTML page rendering
│   │
│   ├── schemas/            # Serialisation/validation schemas
│   ├── services/           # Business logic (no Flask imports)
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JS, images (served by Nginx)
│
├── utils/                  # Shared helpers and decorators
├── tests/                  # All tests mirror app/ structure
├── docker/
│   └── nginx/nginx.conf    # Nginx reverse proxy config
├── documentation/          # API docs, architecture notes
├── docker-compose.yml      # All services: flask, redis, postgres, nginx
├── Dockerfile              # App container build
├── requirements.txt        # Production dependencies
├── .env                    # Secret config — never commit this
├── .env.example            # Template for .env — safe to commit
├── run.py                  # Local dev runner
└── wsgi.py                 # Gunicorn entry point for Docker
```

---

## Getting Started

**1. Clone and set up env**
```bash
git clone <repo-url>
cd DBBD
cp .env.example .env      # fill in your values
```

**2. Start all services with Docker**
```bash
docker compose up --build
```
This starts 4 containers: Flask app, Redis, PostgreSQL, Nginx.

**3. Run locally without Docker**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade                # run migrations
python run.py
```

---

## Environment Variables (`.env`)
| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask secret key |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `FLASK_ENV` | `development` or `production` |
| `JWT_SECRET_KEY` | JWT signing key |

---

## Key Rules for Collaborators

**1. Never import `db`, `cache`, or `jwt` from `app/__init__.py`.**
Always import from `app.extensions`:
```python
from app.extensions import db, cache
```

**2. Keep routes thin.**
Routes call services. Services contain logic. Models contain DB stuff. Nothing else.

**3. One model per file.**
If you add a new table, create a new file in `app/models/` and re-export it in `app/models/__init__.py`.

**4. Cache invalidation rule.**
Any route or service that writes to the DB must delete the relevant cache key immediately after:
```python
db.session.commit()
cache.delete(f"user:{user_id}")  # always invalidate after write
```

**5. Never commit `.env`.**
It is in `.gitignore`. Use `.env.example` to document new variables.

---

## Running Tests
```bash
pytest tests/
```

---
