# BabyLab Project #

## Installation/Deployment Instructions ##

I used the following 2 sets of instructions to deploy the project:

Installation instructions (main): [How To Serve Django Applications with Apache and mod_wsgi on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04)

Postgres/Database Setup (steps 4 and 7, and some of 8 for setting up the DB): [How To Install and Configure Django with Postgres, Nginx, and Gunicorn](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn)

There are many ways to deploy a Django project, perhaps too many ways. I used the first link for deploying the project, due to my familiarity with Apache (and relative ease to setup on Ubuntu). For the first link, ignore using SQL Lite as your datastore. You never want to do that for production. Instead, use the second link, steps 4 and 7 (and part of 8), for setting up Postgres.

The links each vary on where to actually store your project. The first says just in your user home directory, the second says to put it in
`/opt`. Either way will work.

Not in the instructions, but important for the project (and deploying any Django projects in general), is after creating you virtualenv, you will want to install all the python packages needed by the project. These are located in the `requirements.txt` textfile.

In the first link instructions under setting up a virtualenv, the last instruction is type:
`pip install django`

Instead of doing that, type the following command, while your virtualenv is activated:
`pip install -r /path/to/requirements.txt` (django is part of requirements.txt)

## JS/CSS Other code used##

- FontAwesome (v4): [https://fortawesome.github.io/Font-Awesome/](https://fortawesome.github.io/Font-Awesome/)
- Bootstrap (v3): [http://getbootstrap.com/](http://getbootstrap.com/)
- Bootstrap Calendar: [https://github.com/Serhioromano/bootstrap-calendar](https://github.com/Serhioromano/bootstrap-calendar)
- Bootstrap Datepicker: [https://github.com/eternicode/bootstrap-datepicker/](https://github.com/eternicode/bootstrap-datepicker/)
- Bootstrap Timepicker: [https://github.com/jdewit/bootstrap-timepicker](https://github.com/jdewit/bootstrap-timepicker)
- Datatables: [https://www.datatables.net/](https://www.datatables.net/)