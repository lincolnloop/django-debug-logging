Running a Url Test
==================

A management command is included that uses the test client to hit a list of
urls in sequence, allowing them to be logged to the database.  To use it, first
create a list of urls with a new url on each line.  Lines beginning with # are
ignored. ::
    
    # Main urls
    /
    /my/url/
    /my/other/url/
    # Comments
    /my/comment/url/

Then, enable logging and run the *log_urls* management command::

    $ python manage.py log_urls myapp/my_urls.txt

Unless it is run with a verbosity of 0 the command will output status
messages, such as urls that return codes other than 200 and urls that raise
errors.

To run the test as an authenticated user, use the username and password
options::

    $ python manage.py log_urls my_urls.txt --username Legen --password dary

You can also add a name and a description to your run, if you'd like::

    $ python manage.py log_urls my_urls.txt --name "Admin Urls" --description "Urls used by site admins"

If you'd like to conduct a test run with a tool other than the log_urls
management command, you can use the command to manually start and end TestRun
objects, so that your results will be organized correctly in the UI. Before you
conduct your test, simply run::

    $ python manage.py log_urls --manual-start

Then, when you are finished hitting your desired urls::

    $ python manage.py log_urls --manual-end
