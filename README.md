## Campus Jobs
Tracking hours that students work per week.
### Installation
Versions specified below are not required, but the closer they are the more likely it is to work. 
- Python 3.11 with pip 23.2 \
Creating a virtual environment, or "venv", is recommended. \
Within `pip` you should `pip install ...`:
- Django (5.1.6)
- mysqlclient (2.2.7)
- sshtunnel (0.4.0)
- djangorestframework (3.15.2)
- django-crontab (0.7.1)

This project communicates with an external MySQL database, so you need to set one up along with an SSH tunnel to the server MySQL is running on. \
You need to set the following environment variables: \
`NUDBOOSERKEYPATH` - the file path to the SSH private key (debug only)\
`MYSQUEALROOTPASSWORD` - the password for the "root" account in MySQL \
`SECRET_KEY` - the secret key used in deployment (release only) \
For deployment, it is assumed that the application will be running on the same server as the database, so it will try to access it locally instead of through an SSH tunnel. 
### Execution
For debugging, run `python manage.py runserver` in the same directory where manage.py sits.
