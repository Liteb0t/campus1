#!/bin/bash

item='campus1'  # Name of the folder containing the repository
website_directory="/var/www/campusjobs"
server_name="fuze.page"  # IP address or domain of the remote server
scripts_directory="~/scripts" # Contains run-campusjobs.sh
server_user="dbooser"
venv_name="campusvenv"

key_directory=${1:-$NUDBOOSERKEYPATH}  # Optional arg is the location of the ssh key file. Otherwise, use environment variable
current_folder=${PWD##*/}

if [ $current_folder = $item ]; then
	cd ..
fi
tar --exclude='.git' -czvf campus1.tar.gz $item
scp -i $key_directory $item.tar.gz $server_user@$server_name:/var/www/campusjobs/
ssh -i $key_directory $server_user@$server_name "cd $website_directory && rm -rd campus1/ static/; tar -xzvf $item.tar.gz && mv campus1/campus1/settings.py campus1/campus1/settings-debug.py && mv campus1/campus1/settings-deployment.py campus1/campus1/settings.py && source $venv_name/bin/activate && cd campus1 && python manage.py crontab remove && python manage.py crontab add && python manage.py collectstatic && deactivate && sh $scripts_directory/run-campusjobs.sh &"
