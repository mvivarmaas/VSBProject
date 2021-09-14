web: gunicorn VSBProject.wsgi
gunicorn VSBProject:application --preload -b 0.0.0.0:5000
worker: python manage.py process_tasks