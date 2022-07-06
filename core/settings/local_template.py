import dj_database_url
import sys


TEST_DB_URL = 'insert your test DB URL here if needed'
STAGING_DB_URL = 'insert your staging DB URL here if needed'
PROD_DB_URL = 'insert your production DB URL here'

"""
If you're hosting on Heroku, Django won't have permission to create a test
database when running unit tests. Set up your own here and then don't forget
to attach the --keepdb flag to your command when running unit tests.
"""
if 'test' in sys.argv:
    DEFAULT_CONNECTION = dj_database_url.parse(TEST_DB_URL)
    DEFAULT_CONNECTION['TEST'] = {'NAME': 'insert your Test DB name here'}
else:
    db_choice = input('Which DB do you want to connect to?\nType "prod" for Production, "test" for Testing or anything else for Staging.')
    if db_choice == 'prod':
        DEFAULT_CONNECTION = dj_database_url.parse(PROD_DB_URL)
    elif db_choice == 'test':
        DEFAULT_CONNECTION = dj_database_url.parse(TEST_DB_URL)
    else:
        DEFAULT_CONNECTION = dj_database_url.parse(STAGING_DB_URL)

DATABASES = {'default': DEFAULT_CONNECTION}
