# local_settings.py
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
                  'options': '-c search_path=django,prod'
                   },
        'NAME': 'esoprescom_db',
        'USER': 'soprescom_db_user',
        'PASSWORD': 'Soprescom@22024',
        'HOST': '172.20.17.60',
        'PORT': '5432',
    },
    #'sqlLite': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR,'old_soprescom_ecommerce.db'),
    #},
    
    #'mysql': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'sotelma',
    #    'USER': 'db_admin',
    #    'PASSWORD': 'c5vc5V5G7LYU6wm4',
    #    'HOST': '172.20.17.44',
    #    'PORT': '3306',
    #},
    #'ENGINE': 'django.db.backends.postgresql_psycopg2',
    
}
