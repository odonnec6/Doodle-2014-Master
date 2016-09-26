Doodle2014
==========

Software Engineering 2014 project repo.

To run the project locally on your machine ensure python is installed with pip.

Run "pip install -r requirements.txt" to install all dependencies.

To set up the SQLite database, run "python doodle/manage.py syncdb". You will be prompted to create a super user for the database.

Once the database file has been created run "python doodle/manage.py migrate poll" and "python doodle/manage.py migrate comment". This is done to initialise the database models.

To run the website locally, initiate the local server by running "python doodle/manage.py runserver".

The project also contains a file cronTab.py which is used to remove all data for polls that are older than 30 days. Ideally this file will be scheduled to run daily using cron.

To deploy to a production server follow the official Django documentation.
https://docs.djangoproject.com/en/dev/howto/deployment/
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
