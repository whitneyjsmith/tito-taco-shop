"""
Django production settings for core project
"""
import os
import dj_database_url
import json

DEBUG = True if (os.environ.get("DEBUG", "true").lower() == "true") else False

SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
SLACK_SCOPE = os.environ.get('SLACK_SCOPE')

SLACK_PIPELINES = os.environ.get('SLACK_PIPELINES') # json.loads?

TACO_DAILY_LIMIT = os.environ.get('taco_daily_limit')
TITO = os.environ.get('TITO')

# Google Cloud Storage
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE')

# writing google credentials to file
GOOGLE_CREDENTIALS = os.environ.get('GOOGLE_CREDENTIALS')
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS')
if GOOGLE_CREDENTIALS and GOOGLE_APPLICATION_CREDENTIALS:
    with open(GOOGLE_APPLICATION_CREDENTIALS, 'w') as fd:
        fd.write(GOOGLE_CREDENTIALS)


# Databases
DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get('DATABASE_URL'))
DATABASES = {'default': DEFAULT_CONNECTION}


NOTIFICATION_SETTINGS = json.loads(os.environ.get('NOTIFICATION_SETTINGS'))
