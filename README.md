# Campus Jobs
Tracking hours that students work per week.
## Running a debug build
Versions specified below are not required, but the closer they are the more likely it is to work. 
- Python 3.11 with pip 23.2 \
Creating a virtual environment, or "venv", is recommended. \
Within `pip` you should `pip install ...`:
- Django (5.1.6)
- mysqlclient (2.2.7)
- sshtunnel (0.4.0)
- djangorestframework (3.15.2)
- django-crontab (0.7.1)

This project communicates with an external MySQL database, so you need to set one up along with an SSH tunnel to the server MySQL is running on. Alternatively you can modify the `settings.py` to use a local database such as SQLite. \
You need to set the following environment variables: \
`NUDBOOSERKEYPATH` - the file path to the SSH private key (debug only)\
`MYSQUEALROOTPASSWORD` - the password for the "root" account in MySQL \
`SECRET_KEY` - the secret key used in deployment (release only) \
For deployment, it is assumed that the application will be running on the same server as the database, so it will try to access it locally instead of through an SSH tunnel. 

Run `python manage.py runserver` in the same directory where manage.py sits.

## Deployment Guide
This guide is for deploying to a Linux server.
You will need:
- Nginx
- Python 3
- MySQL
- [Optional] Postfix
First, create a database in MySQL named campoos (don't ask), using the "root" MySQL account.
Next, make an environment variable `MYSQUEALROOTPASSWORD` [sic]. Set this to the password of the root MySQL account. Make sure the variable is system-level rather than user-level, or else `django-crontab` won't work.
[Optional] Create a dedicated user called dbooser.
Now create a folder named `campusjobs` in the `/var/www/` directory. You can use another name, but that would require further modification to the deployment script.
Within the new folder, create a Python virtual environment named campusvenv. Pip install the following libraries:
- Django
- djangorestframework
- mysqlclient
- django-crontab
- gunicorn
- [Optional] sshtunnel (if connecting to the database remotely)

Create a folder in your home directory called scripts. Copy the `run-campusjobs.sh` file here. Make a cron task that starts this file on reboot.
Write a reverse proxy in Nginx. By default, the Django server will run the server on localhost:8000. To change the port, modify `run-campusjobs.sh` and edit the `--bind` argument on the last line.
Generate an SSH key pair and configure it so that the user account on the server accepts that key. You can do it, you're a technical guy/girl. [Optional] On your machine, set the environment variable `NUDBOOSERKEYPATH` to the absolute path of the private key file.
`deploycampus.sh` is the bash file you run on your machine which deploys to the server in one command. Configure the variables near the top of this file to work with the server. If you stuck to the recommended names, you won't need to change much at all.
Finally, to deploy, run the shell file from either within the repository folder or one level above:
`sh deploycampus.sh <arg1>`
arg1, which is optional if you set `NUDBOOSERKEYPATH` earlier, takes the path to the ssh key file.
The final output should look similar to this:
Type ctrl+c to exit the script. The web server will continue to run.
E-mail functionality
By default, the web server expects a postfix server running locally and port 25 to be open. If using this option, edit `DEFAULT_FROM_EMAIL` in `campus1/settings-deployment.py` to use your domain instead of `fuze.page`.	
Alternatively, configure the same settings file for Django to connect to an external SMTP server.
