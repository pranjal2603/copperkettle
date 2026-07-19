Copper Kettle
A full-stack café ordering platform built with Django — menu browsing, cart & checkout, online payments, table reservations, reviews, and order tracking, all backed by a fully admin-manageable content system.
🔗 Live demo: https://copperkettle.onrender.com 💻 Repo: https://github.com/pranjal2603/copperkettle.git

Overview
Copper Kettle isn't a static "menu website" — it mirrors how a real café would operate online. A customer can browse the menu, add items to a cart, reserve a table, check out, pay via Razorpay, and track their order status — all without the café owner touching a line of code, since every piece of content (menu, prices, categories, gallery photos) is managed through the Django admin.
Features
Digital menu — categorized (Coffee, Tea, Cold Beverages, Sandwiches, Pizza, Pasta, Burgers, Sides, Desserts), with veg/non-veg indicators and signature items highlighted on the homepage
Cart & checkout — session-based cart, add/remove/increase/decrease quantities, live totals
Payments — Razorpay integration with server-side payment verification
Order tracking — customers can view live order status; a JSON status endpoint powers real-time updates without a page reload
Table reservations — date/time/party-size booking form, tracked and manageable from admin, with optional WhatsApp notification via Twilio
Reviews — star-rating and written reviews from customers
Gallery — photo gallery managed entirely from admin
Contact form — messages saved to the database and visible in admin
Fully admin-driven — every menu item, category, gallery image, and order can be managed from /admin/ with no code changes
Tech Stack
Layer
Technology
Backend
Django 5.2
Database
SQLite (dev) / PostgreSQL (production, via dj-database-url + psycopg2)
Media storage
Cloudinary (production), local filesystem (dev)
Static files
WhiteNoise
Payments
Razorpay
Notifications
Twilio (WhatsApp)
Server
Gunicorn
Deployment
Render

Project Structure
copperkettle/
├── cafe/                  # Main app — models, views, templates
│   ├── models.py          # MenuCategory, MenuItem, GalleryImage, Reservation,
│   │                      # Review, ContactMessage, Order, OrderItem
│   ├── views.py
│   ├── urls.py
│   └── templates/cafe/
├── copperkettle/           # Project settings
├── static/                 # CSS, images
└── requirements.txt

Local Setup
git clone <your-repo-url>
cd copperkettle

python -m venv venv
source venv/bin/activate       # on Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_menu         # adds sample menu items
python manage.py createsuperuser   # create your admin login

python manage.py runserver

Visit http://127.0.0.1:8000/ for the site and http://127.0.0.1:8000/admin/ to manage content.
Environment variables
Create a .env file in the project root for local development:
SECRET_KEY=your-django-secret-key
DEBUG=True

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
⚠️ Never commit .env — it's already listed in .gitignore.
Adding Real Content
Log into /admin/
Add MenuCategory entries (e.g. Coffee, Food, Desserts) with an order value to control sequence
Add MenuItem entries under each category — mark items as is_signature to feature them on the homepage
Add GalleryImage entries with real photos
Reservations, reviews, contact messages, and orders placed on the site all appear in their respective admin sections
Deployment
Deployed on Render:
gunicorn and whitenoise handle the production server and static files
DEBUG = False with ALLOWED_HOSTS configured for the live domain
PostgreSQL database provisioned on Render, connected via DATABASE_URL
Media files (menu photos, gallery images) served through Cloudinary rather than local disk, since Render's filesystem isn't persistent
Environment variables (Razorpay keys, Cloudinary credentials, Twilio credentials, SECRET_KEY) set in the Render dashboard
Migrations run against the live database on deploy
Customizing the Design
All styling lives in static/css/style.css — color variables are defined at the top (--cream, --espresso, --gold, etc.) so the whole palette can be changed from one place.
What I Learned
Building and deploying this project meant going beyond tutorial-level Django and dealing with real production concerns:
Media storage in production (local filesystem doesn't persist on Render — solved with Cloudinary)
Managing environment-specific settings (DEBUG, ALLOWED_HOSTS, database URLs) across dev and production
Running migrations safely against a live database
Integrating and testing a real payment gateway (Razorpay) end-to-end, including server-side signature verification
Building a session-based cart system and connecting it to order tracking with a live-updating status endpoint
License
This project is for portfolio and educational purposes.

