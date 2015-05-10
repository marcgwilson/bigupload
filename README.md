`$ export DJANGO_SETTINGS_MOUDLE=bigupload.settings.dev`

`$ mkvirtualenv bu`

`$ pip install -r requirements.txt`

`$ ./manage.py syncdb`

`$ ./manage.py runserver 0:8000`

To test the API endpoint using Python, simply run `./send.py` in a separate terminal window.
To test the HTML5 file uploader, visit `http:0.0.0.0:8000/` in your browser.

There's also an included testing file named 001.mov for testing the API using python and the browser.