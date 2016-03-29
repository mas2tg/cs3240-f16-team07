=========================
Django admin account info
=========================
NOTE: Remove this section prior to public release.
NOTE: Run python script 'create_django_admin_account.py' to initialize Django admin account.
Username: admin
Password: admin
Access URL: /admin/

=====================================
Explanation of directory organization
=====================================
----- Directories -----
/media/ - pictures videos etc. external to core site components
/static/ - CSS, Javascript, images (i.e. icons favicons logos)
/templates/ - HTML and other webpage files
----- Django Apps -----
safecollab (main site)
reports
users



============
Django notes
============
python manage.py startapp "APP_NAME"	[Creates new Django app]
python manage.py syncdb			[Creates new database to reflect models.py, deprecated as of Django 1.7 in favor of migrate / makemigrations]
python manage.py makemigrations		[Creates migrations to be executed by 'migrate']
python manage.py migrate		[Looks at the INSTALLED_APPS and creates necessary database tables]
python manage.py runserver		[Starts Django test server]
python manage.py flush			[Clear database tables]

==========
psql notes
==========
For initial setup to enable development, open psql command line and enter the following commands:
CREATE DATABASE safecollab;
CREATE USER admin WITH SUPERUSER PASSWORD 'admin';
GRANT ALL PRIVILEGES TO DATABASE safecollab TO admin;