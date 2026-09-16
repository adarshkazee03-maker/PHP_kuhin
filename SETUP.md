# KUHIN Website Setup Complete! ✅

## Project Location
**Mac:** `/Users/adarshthapa/Desktop/KUHIN`

## What's Been Set Up

### ✅ Django Project & Apps
- **kuhin_project/** - Main Django project
- **home/** - Main app with all page views
- **members/** - Team member management
- **events/** - Event management
- **gallery/** - Image gallery
- **resources/** - Resource library

### ✅ Database
- SQLite database configured
- 4 models created and migrated:
  - Member (team profiles)
  - Event (events & activities)
  - GalleryImage (photos)
  - Resource (learning materials)

### ✅ Frontend
- **Base template** - Responsive layout with Bootstrap 5
- **7 Page templates** - Home, About, Team, Events, Gallery, Resources, Contact
- **CSS styling** - Modern, responsive design
- **JavaScript** - Smooth scrolling, form handling, back-to-top button

### ✅ Admin Panel
- All models registered and configured
- Admin filters, search, and ordering set up
- Ready for content management

## Quick Start Guide

### 1. Start the Development Server
```bash
cd /Users/adarshthapa/Desktop/KUHIN
source venv/bin/activate
python manage.py runserver
```

OR use the startup script:
```bash
./start.sh
```

### 2. Access the Website
- **Website:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin

### 3. Create Admin Account (First Time Only)
```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: admin
- Email: admin@kuhin.edu.np  
- Password: [Choose a secure password]

### 4. Log into Admin Panel
- URL: http://127.0.0.1:8000/admin
- Use your created username and password

## Managing Content

### Add Team Members
1. Go to Admin → Members → Add Member
2. Fill in details (name, position, bio, photo)
3. Upload profile photo (optional)
4. Save

### Create Events
1. Go to Admin → Events → Add Event
2. Fill event details (title, date, time, location)
3. Set "Is upcoming" toggle
4. Upload event image (optional)
5. Save

### Add Gallery Images
1. Go to Admin → Gallery Images → Add Gallery Image
2. Upload image
3. Add title and description
4. Select category
5. Save

### Add Resources
1. Go to Admin → Resources → Add Resource
2. Add title, description, category
3. Paste external link (URL)
4. Save

## Project Structure
```
KUHIN/
├── venv/                    # Virtual environment
├── static/
│   ├── css/style.css       # Main stylesheet
│   ├── js/script.js        # JavaScript
│   └── images/             # Images folder
├── media/                   # Uploaded files
├── templates/
│   ├── base.html           # Base template
│   ├── home/index.html     # Home page
│   ├── about.html
│   ├── team.html
│   ├── events.html
│   ├── gallery.html
│   ├── resources.html
│   └── contact.html
├── home/                    # Home app
├── members/                 # Members app
├── events/                  # Events app
├── gallery/                 # Gallery app
├── resources/               # Resources app
├── kuhin_project/           # Django settings
├── manage.py
├── db.sqlite3              # Database
├── requirements.txt        # Dependencies
├── README.md               # Documentation
├── SETUP.md               # This file
└── start.sh               # Startup script
```

## Key URLs
| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/about/ | About page |
| http://127.0.0.1:8000/team/ | Team members |
| http://127.0.0.1:8000/events/ | Events list |
| http://127.0.0.1:8000/gallery/ | Photo gallery |
| http://127.0.0.1:8000/resources/ | Resource library |
| http://127.0.0.1:8000/contact/ | Contact page |
| http://127.0.0.1:8000/admin/ | Admin panel |

## Important Commands

### Run Development Server
```bash
python manage.py runserver
```

### Create Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Shell Access (for debugging)
```bash
python manage.py shell
```

## Troubleshooting

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Next Steps

1. **Customize Logo & Branding**
   - Replace colors in `static/css/style.css`
   - Update footer information in `templates/base.html`

2. **Add Team Members**
   - Go to admin panel
   - Add your club members with photos

3. **Create Events**
   - Add upcoming and past events
   - Include dates, times, and descriptions

4. **Build Resource Library**
   - Add links to research papers
   - Add tools and tutorials

5. **Setup Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial KUHIN website setup"
   ```

6. **Deploy to PythonAnywhere or Heroku**
   - Follow deployment guides in README.md

## Technologies Used

- **Backend:** Django 6.0
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Database:** SQLite (development), PostgreSQL (production)
- **Image Processing:** Pillow
- **Icons:** Font Awesome
- **Server:** Gunicorn (production), Django dev server (development)

## File Conventions

- **Python files:** snake_case (home_page.py)
- **Templates:** use _ for folders (templates/home/index.html)
- **CSS classes:** use - (class="btn-primary")
- **Migrations:** Auto-generated, don't edit manually

## Security Notes (Before Production)

1. Change `SECRET_KEY` in `kuhin_project/settings.py`
2. Set `DEBUG = False`
3. Add your domain to `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Set up HTTPS
6. Use PostgreSQL instead of SQLite
7. Configure proper CORS headers

## Support & Help

- Django Docs: https://docs.djangoproject.com/
- Bootstrap Docs: https://getbootstrap.com/
- Contact: contact@kuhin.edu.np

## Team Members
- Senior 1: Project Lead
- Senior 2: Backend Development ✅
- Senior 3: Frontend Development
- Junior A: Design & Media
- Junior B: Content & Research
- Junior C: Documentation & Testing

---

**🎉 Setup Complete! Start building amazing things with KUHIN! 🎉**

**Built with Django by KUHIN Tech Team 2024**
