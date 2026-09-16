release: python manage.py migrate --settings=kuhin_project.settings.prod && python manage.py collectstatic --no-input --settings=kuhin_project.settings.prod
web: gunicorn kuhin_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --worker-class sync --timeout 120
