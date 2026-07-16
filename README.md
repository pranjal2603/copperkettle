# Copper Kettle

A premium cafe website built with Django — digital menu, table reservations, gallery, and contact form, all manageable through the Django admin.

## Features
- Homepage with signature menu highlights and reservation CTA
- Full menu grouped by category, with veg/non-veg indicators
- Table reservation form (saved to database, status tracked in admin)
- Gallery page
- Contact form
- Everything editable via `/admin/` — no code changes needed to update menu items, prices, or gallery photos

## Setup

```bash
cd copperkettle
python -m venv venv
source venv/bin/activate       # on Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_menu     # adds sample menu items so the site isn't empty
python manage.py createsuperuser   # create your admin login

python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to manage content.

## Adding real content
1. Log into `/admin/`
2. Add `MenuCategory` entries (e.g. Coffee, Food, Desserts) with an `order` value to control sequence
3. Add `MenuItem` entries under each category — mark a few as `is_signature` to feature them on the homepage
4. Add `GalleryImage` entries with real photos
5. Reservations and contact messages submitted on the site will appear under their respective sections in admin

## Deployment
This project is ready to deploy to Railway.app or Render, following the same pattern used for the AlumniConnect project:
1. Add `gunicorn` and `whitenoise` to requirements
2. Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `settings.py`
3. Push to GitHub, connect the repo on Railway/Render, set environment variables
4. Run migrations on the deployed instance

## Customizing the design
All styling lives in `static/css/style.css` — color variables are defined at the top (`--cream`, `--espresso`, `--gold`, etc.) so the whole palette can be changed from one place.
