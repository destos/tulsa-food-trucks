tulsa-food-trucks
=================

requirements
------------

* future requirements
  * PostgresSql
  * PostGIS
  * Python friendly environment

* current requirements
  * a db of some sort
  * python

Installation
------------

**Install Postgres and PostGist on OSX**

**if on OSX 10.8 when install all the things with brew!**

```$ brew install postgis libgeoip gdal```

Setup a virtual environment if you need to.

Copy the ```settings_local.template.py```_file loaded in the tft/tft directory to ```settings_local.py```

Edit the settings file with any local settings, update the default database to a mysql or sqlite one for now.

change to the ```tft``` directory

```$ ./manage.py syncdb```

to create initial user and settings

```$ ./manage.py migrate```

to get all the other models setup.

You should be able to use runserver to start things up.

```$ ./manage.py runserver```

These instructions are not guaranteed to work…
