#!/bin/bash

key_directory=${1:-$NUDBOOSERKEYPATH} # Optional arg is the location of the ssh key file. Otherwise, use environment variable
current_folder=${PWD##*/}
if [ $current_folder = "campus1" ]; then
	cd ..
fi
website_directory="/var/www/campusjobs"
item='campus1'
tar --exclude='.git' -czvf $item.tar.gz $item
scp -i $key_directory $item.tar.gz dbooser@fuze.page:/var/www/campusjobs/
ssh -i $key_directory dbooser@fuze.page "cd $website_directory && rm -rd campus1/ static/; tar -xzvf $item.tar.gz && mv campus1/campus1/settings.py campus1/campus1/settings-debug.py && mv campus1/campus1/settings-deployment.py campus1/campus1/settings.py && source campusvenv/bin/activate && cd campus1 && python manage.py collectstatic && deactivate && sh ~/scripts/run-campusjobs.sh &"
