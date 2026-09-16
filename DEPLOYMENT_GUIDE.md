# KUHIN Deployment Guide

This guide covers deploying your KUHIN website using the production-ready configuration provided.

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Deployment Options](#deployment-options)
3. [Production Configuration](#production-configuration)
4. [Monitoring](#monitoring)

---

## Local Development Setup

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create .env File
```bash
cp .env.example .env
# Edit .env with your local settings (DEBUG=True, SQLite is default)
```

### 3. Run Migrations
```bash
python manage.py migrate --settings=kuhin_project.settings.dev
```

### 4. Create Superuser
```bash
python manage.py createsuperuser --settings=kuhin_project.settings.dev
```

### 5. Run Development Server
```bash
python manage.py runserver --settings=kuhin_project.settings.dev
```

Visit `http://localhost:8000`

---

## Deployment Options

### Option A: VPS Deployment (Hetzner/DigitalOcean/Linode) — Best Control & Value

#### Server Setup (Ubuntu 22.04)

```bash
# SSH into your server
ssh root@YOUR_SERVER_IP

# Create non-root user
adduser kuhin
usermod -aG sudo kuhin
su - kuhin

# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx \
    certbot python3-certbot-nginx git redis-server ufw

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### PostgreSQL Setup

```bash
sudo -u postgres psql

-- Inside psql:
CREATE DATABASE kuhin_db;
CREATE USER kuhin_user WITH PASSWORD 'strong-password-here';
ALTER ROLE kuhin_user SET client_encoding TO 'utf8';
ALTER ROLE kuhin_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE kuhin_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kuhin_db TO kuhin_user;
\q
```

#### Deploy Code

```bash
cd /home/kuhin
git clone https://github.com/yourusername/KUHIN-web-page-.git kuhin
cd kuhin

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Create .env from example (fill with your production values)
cp .env.example .env
nano .env
```

#### Gunicorn Service Setup

```bash
# Copy the service file
sudo cp kuhin.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable kuhin
sudo systemctl start kuhin

# Check status
sudo systemctl status kuhin
```

#### Nginx Configuration

```bash
# Copy nginx config
sudo cp kuhin_nginx.conf /etc/nginx/sites-available/kuhin

# Edit with your domain
sudo nano /etc/nginx/sites-available/kuhin
# Replace: yourdomain.com with your actual domain

# Enable site
sudo ln -s /etc/nginx/sites-available/kuhin /etc/nginx/sites-enabled/

# Test & reload
sudo nginx -t
sudo systemctl reload nginx
```

#### HTTPS with Let's Encrypt

```bash
# Point your domain's A record to YOUR_SERVER_IP first, then:
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (Certbot handles this automatically)
sudo systemctl enable certbot.timer
```

#### Django Migrations

```bash
cd /home/kuhin/kuhin
source venv/bin/activate
DJANGO_SETTINGS_MODULE=kuhin_project.settings.prod python manage.py migrate
DJANGO_SETTINGS_MODULE=kuhin_project.settings.prod python manage.py collectstatic --no-input
```

#### Future Deployments

```bash
cd /home/kuhin/kuhin
./deploy.sh
# Or manually:
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
DJANGO_SETTINGS_MODULE=kuhin_project.settings.prod python manage.py migrate
DJANGO_SETTINGS_MODULE=kuhin_project.settings.prod python manage.py collectstatic --no-input
sudo systemctl restart kuhin
```

**Recommended Hosts:**
- Hetzner CAX11 (~€4/month) — 2 vCPU, 4GB RAM
- DigitalOcean App Platform or Droplets ($5-20/month)
- Linode Nanode ($5/month) — entry level

---

### Option B: Railway — Easiest Setup (PaaS)

1. Push to GitHub
2. Connect GitHub repo in [Railway.app](https://railway.app)
3. Select Django project template
4. Railway auto-detects `railway.toml` and provisions:
   - PostgreSQL database
   - Redis cache
   - Automatic HTTPS
5. Add environment variables in Railway dashboard:
   - `SECRET_KEY`
   - `ALLOWED_HOSTS`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `CLOUDINARY_*` credentials
6. Auto-deploys on every git push

**Pricing:** $5/month base + usage

---

### Option C: Render — Also Easy (PaaS)

1. Create account at [render.com](https://render.com)
2. New → Web Service → Connect GitHub repo
3. Render auto-detects `render.yaml`
4. Add database using Render PostgreSQL plugin
5. Add environment variables
6. Deploy (free tier available, limited)

**Pricing:** Free tier available; paid from $7/month

---

## Production Configuration

### Required Environment Variables

```bash
# Django
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgres://kuhin_user:PASSWORD@host:5432/kuhin_db

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_EMAIL_RECIPIENT=contact@yourdomain.com

# Cloudinary (for image uploads)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Optional
REDIS_URL=redis://host:6379/1
SENTRY_DSN=https://key@sentry.io/project-id
```

### Email Setup (Gmail Example)

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Generate app-specific password
3. Use this password in `EMAIL_HOST_PASSWORD`

### Cloudinary Setup (Free Tier)

1. Sign up at [cloudinary.com](https://cloudinary.com)
2. Free tier: 25GB storage, 25GB bandwidth/month
3. Go to Dashboard → Copy credentials
4. Add to .env or hosting platform

---

## Monitoring

### Check Production Status

**VPS:**
```bash
sudo systemctl status kuhin
sudo journalctl -u kuhin -n 50              # Recent logs
tail -f /home/kuhin/kuhin/logs/kuhin_production.log
```

**Nginx:**
```bash
sudo tail -f /var/log/nginx/kuhin_error.log
sudo nginx -t                               # Verify config
```

**Database:**
```bash
sudo -u postgres psql -d kuhin_db -c "SELECT * FROM auth_user;"
```

### Error Tracking (Optional)

Replace `SENTRY_DSN` in prod.py with your Sentry project DSN:
- Sign up: [sentry.io](https://sentry.io)
- Automatic error notifications

### Health Check

```bash
# In urls.py add:
path('health/', views.health_check, name='health_check'),

# View:
def health_check(request):
    return JsonResponse({'status': 'ok'})

# Then test:
curl https://yourdomain.com/health/
```

---

## Troubleshooting

### Static files not loading
```bash
# On server:
python manage.py collectstatic --no-input --clear --settings=kuhin_project.settings.prod
sudo systemctl restart kuhin nginx
```

### 502 Bad Gateway
```bash
# Check Gunicorn socket exists:
ls -la /home/kuhin/kuhin/gunicorn.sock

# Restart service:
sudo systemctl restart kuhin
sudo journalctl -u kuhin -n 20
```

### Database connection failed
```bash
# Test connection:
psql -U kuhin_user -h localhost -d kuhin_db

# In .env, verify DATABASE_URL is correct
```

### Email not working
```bash
# Test in Django shell:
python manage.py shell --settings=kuhin_project.settings.prod
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Hello', 'from@example.com', ['to@example.com'])
```

---

## Next Steps

1. **Custom domain**: Update DNS A record to point to your server/platform
2. **Email verification**: Set up SPF, DKIM, DMARC records
3. **Performance**: Enable caching headers in nginx, use CDN for static files
4. **Backups**: Set up automated PostgreSQL backups
5. **Monitoring**: Use Sentry for error tracking, Uptime Robot for 24/7 monitoring
