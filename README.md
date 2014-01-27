db-conservatory
===============

Run the tests
-------------
coverage run --source=spinner,profiles --omit="*/migrations/*" manage.py test

Start the DB
------------
postgres -D /usr/local/var/postgres
