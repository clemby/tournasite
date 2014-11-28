# Quick setup
Set up a virtualenv; for example, using virtualenvwrapper:

    mkvirtualenv tournasite
    workon tournasite
  
Install requirements

    pip install -r requirements.txt

and, if you want to run tests, dev-requirements:

    pip install -r requirements.txt


You'll need to put local settings in `compo/local_settings.py`. For convenience
a minimal example is provided in `scripts/local_settings_example.py`.

Create a directory for the database:

    mkdir db

Then `syncdb` as usual:

    ./manage.py syncdb


Front-end tools are managed using bower. To install, simply

    bower install


Now you should be ready to run the development server!

    ./manage.py runserver
