export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
gunicorn --bind=0.0.0.0 --workers=4 project.wsgi