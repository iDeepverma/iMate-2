web: daphne imate.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=imate.settings -v2
release: python manage.py migrate
