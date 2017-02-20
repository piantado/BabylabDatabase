# BabyLab Project #

## Installation Instructions ##
(shortened version of instructions from [How To Serve Django Applications with Apache and mod_wsgi on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04) and also [How To Install and Configure Django with Postgres, Nginx, and Gunicorn](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn))

#### Install Packages from the Ubuntu Repositories ####
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip apache2 libapache2-mod-wsgi
```

Install git:
```
sudo apt-get install git
```

While in your home directory, grab database files from GitHub:
```
git clone https://github.com/piantado/BabylabDatabase
```

Rename directory if desired:
```
mv BabylabDatabase babylab_project
```

Go into directory:
```
cd babylab_project
```


#### Setup a python virtual environment ####

```
sudo pip install virtualenv
```

Create a virtual environment in the django project's directory:
```
virtualenv babylab_project_env
```


#### Install PostgreSGL dependencies and PostgresSQL ####

```
sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib
```

Configure PostgresSQL:

```
sudo su postgres
createdb babylab_db
createuser -P babylab
```

Where `babylab` is the new user (you can choose a different username)

"You will now be met with a series of 6 prompts. The first one will ask you for the name of the new user. Use whatever name you would like. The next two prompts are for your password and confirmation of password for the new user. For the last 3 prompts just enter "n" and hit "enter". This just ensures your new users only has access to what you give it access to and nothing else."

Now activate the PostgreSQL command line interface:
```
psql
```

Grant privileges to the new user created:
```
GRANT ALL PRIVILEGES ON DATABASE babylab_db TO babylab;
```

Then log out from postgres:
```
\q
exit
```


#### Install Django and other Python libraries ####
If you're not in your django project directory, go there and then type:
```
source babylab_project_env/bin/activate
```

Install the Baby Lab database project requirements:
```
pip install -r requirements.txt
```

Also install the PostgreSQL adapter for Python:
```
pip install psycopg2
```

Setup and edit `babylab_project/settings.py` file:
- add database name and user login info
- setup static files folder if not using `/var/www/html/static`
- add SECRET_KEY
- add location of where to save log files for any errors (under LOGGING)
- check ROOT_URLCONF and WSGI_APPLICATION to make sure they match with project name

Setup the database schema:
```
python manage.py makemigrations
python manage.py migrate
```


> **Note:**
>
> If you're having issues with migrate, then try:
> ```
> python manage.py makemigrations core
> python manage.py migrate core
> ```
> (ignore any error messages at this point...)
>
> Then also do:
> ```
> python manage.py makemigrations people scheduling study
> ```
> 
> and then run:
> ```
> python manage.py migrate
> ```
> 
> And the database should be set up properly.
> 
> (Based on the solution from: https://code.djangoproject.com/ticket/24524#comment:10)

Create superuser:
```
python manage.py createsuperuser
```

Collect all static content: (only for production mode)
```
python manage.py collectstatic
```

(For the above command, you may need to first login as root (sudo su) and then activate virtualenv in order to have permission to change directory.)


## Deploying the Database ##

#### Development mode ####
Make sure `DEBUG` in `settings.py` is set to `True`. Then run server by using the command:
```
python manage.py runserver 0.0.0.0:8000
```
(You may need to use port 8080 instead.)

You can press `Ctrl+C` to exit out of development.

#### Production mode ####
If still in the python virtual environment, you can deactivate it now:
```
deactivate
```

Make sure `DEBUG` in `settings.py` is set to `False`. Now you can set up Apache so that it's serving the django application:

Get the example Apache virtual host file that's included in the repository, and place it in:
`/etc/apache2/sites-available/000-default.conf`


restart the apache server:
```
sudo service apache2 restart
```

You can now view your active database website on your server.



> **Note:**
> 
> There is a line in the example 000-default.conf file to allow appointments to be visible in the site's calendar mode:
> Header always unset X-Frame-Options
> 
> However, the mod_headers module may not be activated on your server, in which case you will receive an error message that Header is invalid syntax when you restart the server. In that case, you must also run the command:
> ```
> sudo a2enmod headers
> ```
>
> And then restart the server again in order for the addition to work.

> **Note 2:**
> 
> If you encounter any internal server error, check the apache log file for details (most likely located at):
>```
> /etc/apache2/log/error.log
> ```
>
> If any errors occur, you may need to give apache access to the wsgi.py file:
> ```
> cd ~/babylab_project/babylab_project
> sudo chmod a+x wsgi.py
> ```
> 
> You may also need to give write access to the django error log file (located in the same directory):
> ```
> sudo chmod a+w babylab_project.log
> ```

### Other additions to make once the database is setup ###

Add any disabilities that are selected when adding a child to the database. There are two ways to do this:

**(1) Use Fixtures**

You can use django fixtures to add initial data to a database. In the BabyLab Database django project folder, there is a "fixtures" folder. This is where you can store any data you would like to initialize the database with. Currently there is a disability_data.json file which stores the presets we use for the disability list in the database. Django knows where to look for fixture files based on the FIXTURES_DIRS in settings.py.

To load data from this fixture file, you will need to activate the python virtual environment again:
```
source babylab_project_env/bin/activate
```

And then type the command:
```
python manage.py loaddata disability_data.json
```

More information about fixtures can be found at:
https://docs.djangoproject.com/en/1.10/howto/initial-data/

**(2) Use the Admin Panel**

The Admin Panel is accessed via the "Admin" button at the top of the navigation menu after logging into the database website. Under "Core" is "Disabilities", where you can then click "Add" next to it.  Currently we have this setup for the fields
```
(Name | HTML Name | Order) :
Vision/Hearing Loss | vision-hearing | 0
Serious Injury/Illness |injury-illness | 1
```

(HTML name is the text used for referencing the field in HTML; it doesn't have to be any particular name, but it does need to use valid characters for an HTML name)



## Backups for the Database ##

#### Manual Backups ####
If you want to manually backup the database, use the following commands:
```
sudo su postgres
pgdumpall --globals-only > globals.sql
pg_dump babylab_db > babylab_db_backup.sql
```

Where `globals.sql` and `babylab_db_backup.sql` will be saved in the current folder. `globals.sql` stores the users and group roles for the database, while `babylab_db_backup.sql` stores all the database data.


#### Schedule Local Backups ####
Go to `/var/lib/postgresql` (as the postgres user has access to this directory)
Create two directories:
- `scripts`
- `db_backups`

Create a bash script named `babylab_db_backup.sh` in the scripts directory with the following content:
```
#!/bin/bash
cd /var/lib/postgresql/db_backups
pg_dumpall --globals-only > globals.`date +%Y-%m-%d-%H.%M`.sql
pg_dump babylab_db > babylab_db.`date +%Y-%m-%d-%H.%M`.sql
exit
```

Then login as postgres user:
```
sudo su postgres
```

Now create the cron job that will run daily at 1 AM (or whatever time you choose):
```
crontab -e
```

Select any text editor, and then add the following line to the file:
```
 0 1  *   *   *   /var/lib/postgresql/scripts/babylab_db_backup.sh
```

## Restoring Data in the Database ##

To reload data into an empty database, use the commands:
```
psql babylab_db < /path/to/babylab_db_backup.sql
```

If starting completely from scratch, make sure to also load the globals file:
```
psql -f /path/to/globals.sql postgres
```

> **Note about restoring data:**
>
> (directly from https://www.postgresql.org/docs/9.2/static/backup-dump.html)
> 
> "Before restoring an SQL dump, all the users who own objects or were granted permissions on objects in the dumped database must already exist. If they do not, the restore will fail to recreate the objects with the original ownership and/or permissions. (Sometimes this is what you want, but usually it is not.)
> 
> By default, the psql script will continue to execute after an SQL error is encountered. You might wish to run psql with the ON_ERROR_STOP variable set to alter that behavior and have psql exit with an exit status of 3 if an SQL error occurs:
> ```
> psql --set ON_ERROR_STOP=on dbname < infile
> ```
> Either way, you will only have a partially restored database. Alternatively, you can specify that the whole dump should be restored as a single transaction, so the restore is either fully completed or fully rolled back. This mode can be specified by passing the -1 or --single-transaction command-line options to psql. When using this mode, be aware that even a minor error can rollback a restore that has already run for many hours. However, that might still be preferable to manually cleaning up a complex database after a partially restored dump."
> 
> *The fix so far for our data has been to load the file twice in order for it to populate all the data!*

If you're testing out if this process works, you can manually clear the database (only the data in the database, not the tables themselves) by using the command:
 ```
 python manage.py flush
 ```

 ## JS/CSS Other code used##

- FontAwesome (v4): [https://fortawesome.github.io/Font-Awesome/](https://fortawesome.github.io/Font-Awesome/)
- Bootstrap (v3): [http://getbootstrap.com/](http://getbootstrap.com/)
- Bootstrap Calendar: [https://github.com/Serhioromano/bootstrap-calendar](https://github.com/Serhioromano/bootstrap-calendar)
- Bootstrap Datepicker: [https://github.com/eternicode/bootstrap-datepicker/](https://github.com/eternicode/bootstrap-datepicker/)
- Bootstrap Timepicker: [https://github.com/jdewit/bootstrap-timepicker](https://github.com/jdewit/bootstrap-timepicker)
- Datatables: [https://www.datatables.net/](https://www.datatables.net/)





