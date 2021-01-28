#!/bin/sh
echo "starting mongodb"
/usr/bin/mongod --logpath /var/log/mongod.log &

# start market collector service
echo "starting market collector service"
python3 /app/wealthy_api/market-collector-service/app.py &

# start wealth-service
echo "starting django api ..."
until cd /app/wealthy_api/wealth-service
do
	echo "waiting for django volume..."
done

until python3 manage.py migrate
do
	echo "Waiting for db migration to be ready..."
done

python3 manage.py collectstatic --noinput

gunicorn wealth.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
echo "done."