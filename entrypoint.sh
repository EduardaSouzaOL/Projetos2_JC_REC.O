#!/bin/bash

set -e 

export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

cd /home/site/wwwroot

echo "A executar migrações (migrate)..."
/home/site/wwwroot/antenv/bin/python manage.py migrate --noinput

echo "Migrações concluídas. A iniciar o Gunicorn..."
gunicorn --bind=0.0.0.0 --workers=4 --timeout 120 project.wsgi