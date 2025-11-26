# Django Emerging Tech Project

A minimal README to help a new developer get this Django project running locally.

**Overview**
- **Project:** Django collage web app 
- **Database:** SQLite (`db.sqlite3` included)

**Requirements**
- **Python:** 3.10+ (3.11 recommended)
- **Python packages:** listed in `requirements.txt`

Current contents of `requirements.txt`:

```
asgiref==3.11.0
Django==5.2.8
sqlparse==0.5.3
tzdata==2025.2
```

**Quick Start (PowerShell)**
- Create and activate a virtual environment, install dependencies, run migrations, and start the dev server:

```powershell
# create venv
python -m venv .venv
# activate venv
.\.venv\Scripts\Activate.ps1
# upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt
# apply migrations
python manage.py migrate
# (optional) create admin user
python manage.py createsuperuser
# start development server
python manage.py runserver
```

**Run tests**

```powershell
python manage.py test
```

**Development notes**
- The Django app configuration and routes live under the `collageapp` and `core` packages.
- Static files are under the `static/` directory and templates in `templates/`.
- For production, set `DEBUG=False` and provide a secure `SECRET_KEY` in environment variables or a `.env` loader.

**Troubleshooting**
- If you see package compatibility issues, confirm your Python version with `python --version` and try Python 3.11.
- If migrations fail, you can inspect `core/migrations/` and re-run `python manage.py migrate`.

If you want, I can also add a `Makefile`/PowerShell script or a `dev` task to simplify these steps.
