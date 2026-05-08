# Portfolio Site — Omolade Famuyide

A full-featured personal portfolio website built with Django, featuring an AI chatbot, Google Calendar appointment booking, and a fully admin-managed content system.

---

## Features

- **Home** — hero section, featured projects, skills preview, and live stats
- **About** — personal bio and background managed via the admin panel
- **Projects** — detailed project showcase with problem/solution/outcome, image gallery, and demo videos
- **Skills** — categorised skill list with proficiency levels
- **Resume** — professional timeline (education, experience, certifications, achievements) with PDF download
- **Contact** — contact form with email notification + appointment booking with Google Calendar integration
- **AI Chatbot (Dee)** — Gemini 2.0 Flash-powered assistant that answers visitor questions about the portfolio
- **Site visit tracking** — middleware logs page visits to the database
- **Django Admin** — all content is fully manageable without touching code

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6 |
| Database | SQLite |
| AI | Google Gemini 2.0 Flash |
| Calendar | Google Calendar API (Service Account) |
| Email | Gmail SMTP (App Password) |
| Image handling | Pillow |
| Frontend | HTML, CSS, JavaScript |

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/2026-Spring-5V98/Portfolio_Site_OmoladeFamuyide.git
cd Portfolio_Site_OmoladeFamuyide
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create secret config files

Copy each example file and fill in your own credentials:

```bash
cp secret_key.example.py secret_key.py
cp email_config.example.py email_config.py
cp gemini_config.example.py gemini_config.py
cp gcal_config.example.py gcal_config.py
cp gcal_credentials.example.json gcal_credentials.json
```

> These files are gitignored and must never be committed.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — manage all content at `http://127.0.0.1:8000/admin`.

---

## Environment / Config Files

| File | Purpose |
|------|---------|
| `secret_key.py` | Django `SECRET_KEY` |
| `email_config.py` | Gmail address and app password |
| `gemini_config.py` | Google Gemini API key |
| `gcal_config.py` | Google Calendar ID and timezone |
| `gcal_credentials.json` | Google service account key (JSON) |

---

## Project Structure

```
Portfolio/
├── MainApp/
│   ├── models.py          # Profile, Project, Skill, Resume, Appointment, etc.
│   ├── views.py           # Page views + Gemini chatbot API
│   ├── forms.py           # Contact and appointment forms
│   ├── google_calendar.py # Calendar integration
│   ├── middleware.py      # Site visit tracker
│   ├── templates/         # HTML templates
│   └── static/            # CSS and JS
├── portfolio_site/
│   ├── settings.py        # Django settings
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## Author

**Omolade Famuyide**
