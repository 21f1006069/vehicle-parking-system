# Vehicle Parking App

A full-stack parking management solution that lets users register vehicles, reserve and release parking spots, view history reports, and receive scheduled notifications. Admins can manage lots, spots, and users from the same platform.


- **Backend**: Flask + Celery + SQLite
- **Frontend**: Vue 3 + Vite

---

## 1. Technology Stack

| Layer | Tools & Libraries |
| --- | --- |
| Backend API | Python 3.10+, Flask, Flask-RESTX, Flask-Session |
| Task queue | Celery, Redis (or another broker) |
| Database | SQLite (default), SQLAlchemy helpers |
| Auth & security | bcrypt, python-dotenv |
| Notifications | Google Chat Webhook, SMTP, optional SMS/email services |
| Frontend | Node.js 18+, Vite, Vue 3, Axios, Bootstrap 5 |

> All backend dependencies are listed in `requirements.txt`; frontend dependencies are in `frontend/package.json`.

---

## 2. Prerequisites

Install the following on your machine:

- Python 3.10 or newer
- Node.js 18+ and npm
- Redis (for Celery broker/result backend) or update Celery config to match your environment
- Git (optional but recommended)

---

## 3. Backend Setup

```bash
# 1) Clone or download the repository
git clone https://github.com/your-org/vehicle-app.git
cd vehicle-app

# 2) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows PowerShell: .\venv\Scripts\Activate.ps1

# 3) Install backend dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4) Create the SQLite database (first run only)
python app.py  # or run a helper script if you have one
```

### Environment Variables

Create a `.env` file in the project root with the values you need:

```
SECRET_KEY=change-me
SESSION_TYPE=filesystem
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=mailer@example.com
SMTP_PASS=super-secret
GC_WEBHOOK_URL=https://chat.googleapis.com/...
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

If you do not configure the optional services (SMTP, Google Chat), related features will simply no-op.

### Running the Flask API

```bash
source venv/bin/activate
flask --app app.py run --debug
# or python app.py
```

The backend listens on `http://localhost:5000` by default.

---

## 4. Frontend Setup (Vue + Vite)

```bash
cd frontend
npm install

# Start the dev server
npm run dev
```

The frontend uses the Vite dev server (default `http://localhost:5173`) and proxies API calls to the Flask backend at `http://localhost:5000`. Adjust `src/api.js` if your backend runs elsewhere.

To build a production bundle:

```bash
npm run build
npm run preview   # optional local preview
```

---

## 5. Background Jobs (Celery)

The project schedules reminders, exports, and monthly reports through Celery tasks defined in `tasks.py`.

```bash
# Terminal 1 – Celery worker
source venv/bin/activate
celery -A celery_app.celery worker --loglevel=info

# Terminal 2 – Celery beat scheduler (for periodic jobs)
source venv/bin/activate
celery -A celery_app.celery beat --loglevel=info
```

Make sure Redis (or your chosen broker/result backend) is running before starting these processes.

## 7. Default Credentials
Once seeded, you can log in with the sample admin account:

- Email: `admin@parking.com`
- Password: `admin@123`


