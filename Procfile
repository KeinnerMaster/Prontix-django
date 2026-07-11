release: python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn greenery_project.wsgi --log-file -