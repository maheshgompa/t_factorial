import platform
import json
import os

# Secret file

# with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secrets.json')) as secrets_file:
#     secrets = json.load(secrets_file)
#
# def get_secret(setting, secrets=secrets):
#     """Get secret setting or fail with ImproperlyConfigured"""
#     try:
#         return secrets[setting]
#     except KeyError:
#         raise ImproperlyConfigured("Set the {} setting".format(setting))


if platform.system() == 'Darwin':
    # Development enviroment
    # ------------------------
    # TEMP_FOLDER = '/Users/javierjimenezalvarez/Temp/'
    GRAFANA_RENDER = '' 
    GRAFANA_LINK = '' 
    INGESTION_LOG_FILE = 'ingestion.log' 
    # INGESTION_DATA_FOLDER = '/Users/javierjimenezalvarez/Downloads/DatosDewa/pt1'
    TEMPLATE_FOLDER = ''

    RAW_DATABASE_CONNECTION = {
        "host": "localhost",
        "port": "5432",
        "database": "dewa_pt1_raw",
        "user": "postgres",
        # "password": get_secret('ADMIN_DATABASE_PASSWORD'),
        "password": "root"
    }

    PRODUCTION_DATABASE_CONNECTION = {
        "host": "localhost",
        "port": "5432",
        "database": "dewa_pt1_production",
        "user": "postgres",
        # "password": get_secret('ADMIN_DATABASE_PASSWORD'),
        "password": "root"
    }
else:
    # Production enviroment
    # ------------------------
    # TEMP_FOLDER = ''
    # GRAFANA_RENDER = ''
    # GRAFANA_LINK = ''
    # INGESTION_LOG_FILE = 'ingestion.log'
    # INGESTION_DATA_FOLDER = '/data/data/downloaded/pt1/'
    # INGESTION_DATA_SYNC_FOLDER = '/data/data/current/solution/PT-1/'
    # SYNC_TOOL_PATH = '/data/software/azcopy_linux_amd64_10.18.0/'
    # SYNC_TOOL_COMMAND = './azcopy copy "https://metomodule.blob.core.windows.net/noorenergy1/solution?sp=racwli&st=2023-04-12T07:27:53Z&se=2025-04-01T15:27:53Z&spr=https&sv=2021-12-02&sr=c&sig=%s" /data/data/current --recursive' % get_secret('AZURE_TOKEN')
    # TEMPLATE_FOLDER = ''

    RAW_DATABASE_CONNECTION = {
        "host": "localhost",
        "port": "5432",
        "database": "dewa_pt1_raw",
        "user": "postgres",
        # "password": get_secret('ADMIN_DATABASE_PASSWORD'),
        "password": "root"
    }

    PRODUCTION_DATABASE_CONNECTION = {
        "host": "localhost",
        "port": "5432",
        "database": "dewa_pt1_production",
        "user": "postgres",
        # "password": get_secret('ADMIN_DATABASE_PASSWORD'),
        "password": "root"
    }

