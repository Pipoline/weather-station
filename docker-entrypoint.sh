#!/usr/bin/env sh
cd /srv

# Prepare log files and start outputting logs to stdout
#touch /srv/logs/gunicorn.log
#touch /srv/logs/access.log
#tail -n 0 -f /srv/logs/*.log &

## Start Gunicorn processes
#echo Starting Gunicorn.
#exec gunicorn hello.wsgi:application \
#    --name hello_django \
#    --bind 0.0.0.0:8000 \
#    --workers 3 \
#    --log-level=info \
#    --log-file=/srv/logs/gunicorn.log \
#    --access-logfile=/srv/logs/access.log \
#    "$@"

echo "Starting uwsgi"
uwsgi --ini /etc/uwsgi.ini

echo "Starting nginx"
#python manage.py runserver 0.0.0.0:80
nginx -g 'daemon off;'

