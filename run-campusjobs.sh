#!/bin/sh

# GUNICORN=/usr/bin/gunicorn
GUNICORN=/var/www/campusjobs/campusvenv/bin/gunicorn
ROOT=/var/www/campusjobs/campus1
PID=~/.pid/gunicorn.pid

APP=campus1:application

if [ -f $PID ]; then
	cat $PID
	kill $(cat $PID)
	rm $PID
fi

cd $ROOT
exec $GUNICORN campus1.wsgi --pid=$PID --bind=localhost:8000
