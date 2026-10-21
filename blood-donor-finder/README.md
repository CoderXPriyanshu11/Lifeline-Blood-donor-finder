# LifeLine — Blood Donor Finder
### SPPU SE AI&DS Community Engagement Project (CEP)

> A privacy-first, community-built web platform that connects voluntary blood donors with patients in need — fast, safely, and transparently.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3 (custom variables + responsive), Vanilla JS, Chart.js 4 (CDN) |
| Backend | Python 3.10+, Flask 3 |
| Database | MySQL 8, `mysql-connector-python` (connection pool, raw parameterised SQL) |
| Auth | Flask sessions + Werkzeug `generate_password_hash` / `check_password_hash` |
| Templating | Jinja2 with `base.html` and `admin_base.html` layouts |
| Fonts | Google Fonts: Fraunces (headings), Inter (body), IBM Plex Mono (labels) |

---

## Folder Structure

```
blood-donor-finder/
├── app.py               ← Main Flask application (all routes)
├── config.py            ← Environment-variable-based config
├── db.py                ← MySQL connection pool + query helpers
├── seed_admin.py        ← Creates / updates default admin account
├── schema.sql           ← Full DB schema + demo seed data
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html                 ← Public layout
│   ├── admin_base.html           ← Admin layout
│   ├── index.html                ← Home (stats, steps, campaigns)
│   ├── register.html             ← Donor registration
│   ├── request_blood.html        ← Blood request form
│   ├── search.html               ← Donor search (with privacy masking)
│   ├── campaign.html             ← Public campaign list
│   ├── survey.html               ← Community survey
│   ├── feedback.html             ← Star-rating feedback form
│   ├── thank_you.html            ← Post-submission thank you
│   ├── about.html                ← About, what it does NOT do, privacy
│   ├── admin_login.html          ← Admin sign-in page
│   ├── admin_dashboard.html      ← KPI cards + 6 Chart.js graphs
│   ├── admin_donors.html         ← Donor management (search, toggle, delete)
│   ├── admin_requests.html       ← Request management (status, delete)
│   ├── admin_campaigns.html      ← Campaign CRUD
│   ├── admin_stakeholders.html   ← Stakeholder log CRUD
│   ├── admin_survey.html         ← Survey response table
│   └── admin_feedback.html       ← Feedback table with star display
├── static/
│   ├── css/style.css             ← All styles (design tokens, responsive)
│   └── js/script.js              ← Nav toggle, flash dismiss, confirm
└── docs/
    ├── Community_Survey_Design.md
    ├── Awareness_Campaign_Plan.md
    ├── Stakeholder_Interaction_Log.md
    ├── Feedback_Analysis.md
    └── Project_Impact_Analysis.md
```

---

## Step-by-Step Setup

### 1. Prerequisites

- Python 3.10+
- MySQL 8.0+
- `pip`
- (Optional) `virtualenv` or `venv`

### 2. Create and activate a virtual environment

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the MySQL database

Log in to MySQL and run the schema:

```bash
mysql -u root -p < schema.sql
```

This creates the `blood_donor_finder` database, all tables, and demo seed data.

### 5. Create the admin account

```bash
python seed_admin.py
```

Default credentials: **username:** `admin` | **password:** `Admin@123`

> You should change the password after first login.

### 6. Configure environment variables

Create a `.env` file or set these in your shell before running:

```bash
# .env (do NOT commit to version control)
SECRET_KEY=your-very-long-random-secret-here
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=blood_donor_finder
FLASK_DEBUG=true
```

To load the `.env` file automatically, install `python-dotenv` and add this to `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

Or simply export the variables in PowerShell:

```powershell
$env:DB_PASSWORD = "your_mysql_password"
$env:SECRET_KEY  = "your-secret-key"
```

### 7. Run the development server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

Admin panel: [http://localhost:5000/admin/login](http://localhost:5000/admin/login)

---

## Feature List

### Public

| Feature | Route |
|---------|-------|
| Home with live stats & upcoming camps | `GET /` |
| Donor registration (server-validated, consent required) | `GET/POST /register` |
| Blood request form → redirects to matching search | `GET/POST /request-blood` |
| Donor search (blood group, city, area, availability, compatibility) | `GET /search` |
| Contact details masked publicly | `/search` |
| Community survey | `GET/POST /survey` |
| Star-rating feedback | `GET/POST /feedback` |
| Awareness campaigns (upcoming / completed) | `GET /campaigns` |
| About / What we do NOT do | `GET /about` |

### Admin Panel (`/admin/*`)

| Feature | Route |
|---------|-------|
| Secure login (hashed passwords) | `/admin/login` |
| KPI dashboard + 6 Chart.js graphs | `/admin/dashboard` |
| Analytics JSON endpoint | `/admin/api/analytics` |
| Donor management (search, verify, toggle availability, delete) | `/admin/donors` |
| Request management (status update, delete) | `/admin/requests` |
| Campaign CRUD | `/admin/campaigns` |
| Stakeholder interaction log CRUD | `/admin/stakeholders` |
| Survey response table | `/admin/survey` |
| Feedback table with star display | `/admin/feedback` |

---

## Security Notes for Real Deployment

> The following are **not** implemented in this academic prototype but are essential before any public deployment.

1. **CSRF Protection** — Add `Flask-WTF` and include CSRF tokens in all forms.
2. **HTTPS** — Serve over TLS/HTTPS only. Set `SESSION_COOKIE_SECURE = True`.
3. **Rate Limiting** — Use `Flask-Limiter` to prevent form spam and brute-force login attempts.
4. **Strong Secret Key** — Generate with `python -c "import secrets; print(secrets.token_hex(32))"` and store in an environment variable.
5. **Database User** — Create a dedicated MySQL user with only the minimum required privileges on `blood_donor_finder`; never use `root`.
6. **Input Sanitisation** — All user content rendered via Jinja2's `{{ }}` auto-escapes HTML; parameterised SQL is used everywhere.
7. **Error Pages** — Add custom 404/500 handlers and disable debug mode (`FLASK_DEBUG=false`) in production.
8. **Logging** — Configure a production logger (e.g., to a file or logging service).
9. **Data Backups** — Schedule daily MySQL dumps.
10. **Environment Variables** — Use a secrets manager (AWS Secrets Manager, HashiCorp Vault) rather than `.env` files in production.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `mysql.connector.errors.InterfaceError` | Wrong DB credentials or MySQL not running | Check `DB_HOST`, `DB_USER`, `DB_PASSWORD`, ensure MySQL service is running |
| `RuntimeError: DB pool not initialised` | `init_pool(app)` not called | Ensure `db.py` is imported and `init_pool(app)` is called in `app.py` before first request |
| `TemplateNotFound` error | Template file missing or wrong name | Verify all template files exist in `templates/` |
| `KeyError` in Jinja template | Variable not passed from route | Check the `render_template` call in `app.py` |
| Admin login fails | Admin not seeded | Run `python seed_admin.py` again |
| Charts not loading | Network issue or Chart.js CDN blocked | Download Chart.js and serve from `static/` |
| Phone masking shows wrong output | Phone is not exactly 10 digits | Ensure DB data has 10-digit phone numbers |
| CSS not loading | Static folder path issue | Confirm `static/css/style.css` exists and Flask is run from project root |

---

## CEP Documentation

All Community Engagement Project documentation is in `docs/`:

| File | Contents |
|------|---------|
| `Community_Survey_Design.md` | Survey purpose, instrument, pilot findings, how findings shaped design |
| `Awareness_Campaign_Plan.md` | 3-phase campaign plan with messaging per survey barrier |
| `Stakeholder_Interaction_Log.md` | All stakeholder meetings, decisions influenced |
| `Feedback_Analysis.md` | Collection method, SQL queries, theme tags, pilot themes |
| `Project_Impact_Analysis.md` | Metrics table, before/after plan, limitations, next steps |

---

## License

This project is developed for academic (CEP) purposes at SPPU. Not for commercial use.
