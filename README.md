# KUHIN — Kathmandu University Health Informatics Network

**Production-Ready Website** | Django 4.2 | Bootstrap 5 | Python 3.10+

---

## Quick Start

```bash
# 1. Clone and navigate
git clone <repo> && cd kuhin-web

# 2. Create virtual environment
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your values

# 5. Run migrations
python manage.py migrate --settings=kuhin_project.settings.dev

# 6. Create superuser (for admin panel)
python manage.py createsuperuser --settings=kuhin_project.settings.dev

# 7. Collect static files
python manage.py collectstatic --settings=kuhin_project.settings.dev

# 8. Run development server
python manage.py runserver --settings=kuhin_project.settings.dev
```

Visit `http://127.0.0.1:8000` — Admin at `/admin/`

---

## Project Structure

```
kuhin_project/         ← Django settings (base, dev, prod)
templates/             ← All HTML templates (project-level)
  base.html            ← Unified base template
  home.html            ← Landing page
  about.html, programs.html, team.html
  events.html, event_detail.html
  gallery.html
  resources.html, resource_detail.html
  contact.html
  blogs/               ← Blog templates
  news/                ← Newsletter templates
  components/          ← Reusable partials (pagination)
  404.html, 500.html
static/
  css/kuhin-design-system.css   ← Single design system (all styles)
  js/kuhin.js                   ← Progressive enhancement
  images/Kuhin_logo.png
home/                  ← Main routing app (views, urls, forms)
blog/                  ← Blog posts
events/                ← Events management
members/               ← Team member profiles
gallery/               ← Photo gallery
resources/             ← Resource library
newsletter/            ← News updates & email subscriptions
```

---

## Pages

| Route | View | Template |
|-------|------|----------|
| `/` | `home.home` | `home.html` |
| `/about/` | `home.about` | `about.html` |
| `/programs/` | `home.programs` | `programs.html` |
| `/team/` | `home.team` | `team.html` |
| `/team/<pk>/` | `home.member_detail` | `member_detail.html` |
| `/events/` | `home.events` | `events.html` |
| `/events/<slug>/` | `home.event_detail` | `event_detail.html` |
| `/gallery/` | `home.gallery` | `gallery.html` |
| `/resources/` | `home.resources` | `resources.html` |
| `/resources/<slug>/` | `home.resource_detail` | `resource_detail.html` |
| `/contact/` | `home.contact` | `contact.html` |
| `/blogs/` | `blog.blog_list` | `blogs/blog_list.html` |
| `/blogs/<slug>/` | `blog.blog_detail` | `blogs/blog_detail.html` |
| `/news/` | `newsletter.news_list` | `news/news_list.html` |
| `/news/<slug>/` | `newsletter.news_detail` | `news/news_detail.html` |
| `/subscribe/` | `newsletter.subscribe` | (redirect) |

---

## Design System

All styles live in `static/css/kuhin-design-system.css`.

**Colour Tokens:**
- `--ku-navy` `#0B1F45` — Primary dark
- `--ku-cobalt` `#2952A3` — Primary accent
- `--ku-teal` `#0E8F7A` — Secondary
- `--ku-gold` `#C8973A` — Highlight / CTA

**Components:** `.btn-ku`, `.ku-card`, `.blog-card`, `.event-card`, `.member-card`, `.feature-card`, `.resource-card`, `.page-hero`, `.section-tag`, `.ku-alert`, `.ku-input`, `.ku-label`

---

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use `kuhin_project.settings.prod` settings
3. Configure PostgreSQL database
4. Set `CLOUDINARY_*` values for media storage
5. Run `gunicorn kuhin_project.wsgi:application`
6. Use the included `Procfile`, `render.yaml`, or `railway.toml`

---

## Tech Stack

- **Backend:** Django 4.2, Python 3.10+
- **Frontend:** HTML5, CSS3 (custom design system), Bootstrap 5 grid
- **Fonts:** Syne (headings), DM Sans (body) via Google Fonts
- **Icons:** Font Awesome 6.5
- **Rich Text:** django-ckeditor
- **Static Serving:** WhiteNoise
- **Media Storage:** Cloudinary (production) / Local (development)
- **Deployment:** Gunicorn, Nginx

---

*KUHIN — Kathmandu University Health Informatics Network*
# KUHIN-
# KUHIN-
# KUHIN-
# KUHIN-
